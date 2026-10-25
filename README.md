
# 🤖 AI Data Agent

An interactive data analysis application that helps users explore datasets and ask questions about their data through a web interface. Built with React, FastAPI, LangChain, and LangGraph, the project supports agent-based workflows for SQL analysis and ETL operations.

## 🏗️ Architecture & Workflow

An overview of how the **AI Data Agent** processes requests through FastAPI, LangGraph routing, and specialized sub-agents.

<p align="center">
  <img src="AI%20Data%20Agent%20Workflow%20Diagram.png" alt="AI Data Agent Architecture" width="850">
</p>
## ✨ Features

- **Interactive Web Interface** — Ask questions about your data through a web application.
- **AI Agent Workflow** — Routes user questions to SQL analysis or ETL analysis.
- **FastAPI Backend** — Provides API endpoints for chat, dataset listing, and schema information.
- **Dataset Exploration** — Includes sample datasets for payments, ratings, rides, users, and vehicles.
- **ETL Workflow** — Supports data extraction and transformation workflows.
- **SQL Analysis** — Includes an agent workflow for SQL-related questions.
- **Workflow Visualization** — Includes a graph diagram of the agent workflow.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| FastAPI | REST API |
| LangChain | LLM integration and tools |
| LangGraph | Agent workflow orchestration |
| React | Frontend interface |
| Vite | Frontend development server |
| CSV | Sample datasets |

## 📁 Project Structure

```text
AI-Data-Agent/
├── Models/
│   ├── __init__.py
│   └── schema.py
├── agents/
│   ├── __init__.py
│   ├── data_agent.py
│   ├── etl_analyst.py
│   └── sql_analyst.py
├── api/
│   ├── README.md
│   └── server.py
├── data/
│   ├── extract/
│   ├── transform/
│   ├── payments.csv
│   ├── ratings.csv
│   ├── rides.csv
│   ├── users.csv
│   └── vehicles.csv
├── frontend/
│   ├── src/
│   ├── package.json
│   └── index.html
├── utils/
│   ├── database.py
│   ├── etl_tools.py
│   └── llm_pick.py
├── feed_db.py
├── main.py
├── requirements.txt
├── requirements-web.txt
├── pyproject.toml
├── uv.lock
├── DEPLOYMENT.md
└── data_agent_graph.png
```

## 🚀 Getting Started

### Prerequisites

Install the following tools:

- Python version specified in `.python-version`
- Node.js and npm
- An API key for an LLM provider supported by the current code
- A database, if required by your configuration

### 1. Clone the Repository

```bash
git clone https://github.com/kush788/AI-Data-Agent.git
cd AI-Data-Agent
```

### 2. Set Up the Backend

Create a Python virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create your local environment file.

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**

```bash
cp .env.example .env
```

Open `.env` and configure the variables required by your application. Check `utils/llm_pick.py`, `utils/database.py`, and `DEPLOYMENT.md` for the exact configuration.

> **Security:** Never commit your `.env` file or expose API keys, passwords, or database credentials. Keep `.env.example` limited to safe placeholder values.

Because Groq has been removed, configure another LLM provider supported by the current implementation before using AI-powered features.

### 4. Run the Backend

From the project root, run:

```bash
uvicorn api.server:app --reload --port 8000
```

The backend will be available at:

- **API:** http://localhost:8000
- **Swagger API Documentation:** http://localhost:8000/docs

### 5. Run the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually:

http://localhost:5173

If the frontend requires an API URL, configure it according to `frontend/.env.example` and the frontend source code.

## 🔌 API Endpoints

The backend includes endpoints for these operations. Check the running API documentation at `http://localhost:8000/docs` for exact methods and request formats.

| Endpoint | Description |
|---|---|
| `/api/chat` | Sends a question to the data-agent workflow |
| `/api/datasets` | Lists available datasets |
| `/api/schema` | Retrieves schema information when database configuration permits |

## 📊 Sample Datasets

The project includes CSV datasets for:

- Payments
- Ratings
- Rides
- Users
- Vehicles

These datasets can be used for local development and experimentation. Ensure that all published data is safe to share.

## 🧪 Troubleshooting

### AI requests are failing

- Check your `.env` configuration.
- Verify that the selected LLM provider and model are supported by the code.
- Confirm that your API key is valid and has access to the model.
- Restart the backend after changing environment variables.

### Frontend cannot connect to the backend

- Make sure the backend is running on port `8000`.
- Verify the API URL configured in the frontend.
- Check the browser console and backend terminal for errors.

### Dependency installation fails

- Verify your Python and Node.js versions.
- Activate the virtual environment before installing Python packages.
- Review `requirements.txt`, `frontend/package.json`, and `DEPLOYMENT.md`.

## 🔐 Security Best Practices

- Never commit `.env` or other files containing secrets.
- Do not store API keys directly in source code.
- Review CSV files and diagnostic files before publishing.
- Rotate any credentials accidentally exposed in Git history.

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

## 📄 License

No license is currently specified. Add a `LICENSE` file if you want to define the terms under which others can use and distribute this project.

---

**GitHub Repository:** https://github.com/kush788/AI-Data-Agent
