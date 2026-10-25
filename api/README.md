# FastAPI bridge

Run from the project root:

```bash
uvicorn api.server:app --reload --port 8000
```

Endpoints:
- `GET /api/health`
- `GET /api/datasets`
- `GET /api/files`
- `GET /api/schema`
- `POST /api/chat`
- `POST /api/etl/extract`
