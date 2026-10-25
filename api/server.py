import ast
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

load_dotenv()

# Import after environment loading so the existing agent configuration works.
from agents.data_agent import data_agent
from utils.database import DatabaseUtil

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

app = FastAPI(title="AI Data Agent API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=4000)

class ChatResponse(BaseModel):
    route: str
    answer: str
    sql: str = ""
    safe: bool | None = None
    safety_comments: str = ""
    results: list[dict[str, Any]] = []
    raw_result: str = ""
    timestamp: str

class ETLRequest(BaseModel):
    url: str
    output_folder: str = "data/extract"
    format: str = "csv"


def _parse_rows(raw: str) -> list[dict[str, Any]]:
    if not raw:
        return []
    try:
        value = ast.literal_eval(raw)
        if isinstance(value, list):
            return [{f"column_{i+1}": x for i, x in enumerate(row)} if isinstance(row, tuple) else {"value": row} for row in value]
    except Exception:
        pass
    return []


def _extract_state(response: dict[str, Any], route: str) -> ChatResponse:
    answer = "The agent completed the request."
    sql = ""
    safe = None
    comments = ""
    raw_result = ""
    results: list[dict[str, Any]] = []

    if route == "sql":
        answer = response.get("final_answer") or "I couldn't generate a final answer."
        sql = response.get("generated_sql_query", "")
        safe_value = response.get("is_safe")
        safe = safe_value.lower() == "yes" if isinstance(safe_value, str) else None
        comments = response.get("comments", "")
        raw_result = response.get("sql_query_execution_result", "") or ""
        results = _parse_rows(raw_result)
    else:
        messages = response.get("messages", [])
        if messages:
            last = messages[-1]
            answer = getattr(last, "content", None) or str(last)
        else:
            answer = "ETL operation completed."

    return ChatResponse(
        route=route,
        answer=answer,
        sql=sql,
        safe=safe,
        safety_comments=comments,
        results=results,
        raw_result=raw_result,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AI Data Agent"}

@app.get("/api/datasets")
def datasets():
    items = []
    for path in sorted(DATA_DIR.glob("*.csv")):
        try:
            import pandas as pd
            df = pd.read_csv(path, nrows=5)
            rows = sum(1 for _ in open(path, "rb")) - 1
            items.append({"name": path.stem, "file": path.name, "rows": max(rows, 0), "columns": len(df.columns), "fields": list(df.columns)})
        except Exception as exc:
            items.append({"name": path.stem, "file": path.name, "rows": 0, "columns": 0, "fields": [], "error": str(exc)})
    return items

@app.get("/api/schema")
def schema():
    required = ["host", "port", "user", "password", "database"]
    if not all(os.getenv(k) for k in required):
        return {"connected": False, "message": "Database environment variables are not configured."}
    try:
        obj = DatabaseUtil({"host": os.environ["host"], "port": os.environ["port"], "user": os.environ["user"], "password": os.environ["password"], "dbname": os.environ["database"]})
        details = obj.schema_details("public")
        return {"connected": True, "details": details}
    except Exception as exc:
        return {"connected": False, "message": str(exc)}

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        response = data_agent.invoke({"messages": [HumanMessage(content=payload.message)], "route_response": ""})
        route = response.get("route_response", "sql")
        return _extract_state(response, route)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/api/etl/extract")
def etl_extract(payload: ETLRequest):
    if payload.format not in {"csv", "json", "parquet"}:
        raise HTTPException(status_code=400, detail="format must be csv, json, or parquet")
    from utils.etl_tools import ETLTools
    try:
        message = ETLTools().extract_load(payload.url, payload.output_folder, payload.format)
        return {"success": "successfully" in message.lower(), "message": message}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/files")
def files():
    result = []
    for folder in [DATA_DIR / "extract", DATA_DIR / "transform"]:
        folder.mkdir(parents=True, exist_ok=True)
        for path in folder.iterdir():
            if path.is_file():
                result.append({"name": path.name, "folder": folder.name, "size": path.stat().st_size})
    return result
