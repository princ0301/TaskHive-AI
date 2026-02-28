# Multi-Agent AI Research System

An end-to-end multi-agent system that researches any topic and generates a professional report — automatically.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-0.28.8-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal)
![Streamlit](https://img.shields.io/badge/Streamlit-1.34-red)

---

## Architecture

```
User (Streamlit UI)
        ↓
FastAPI Backend  ←→  SQLite DB
        ↓
  CrewAI Pipeline
        ↓
Researcher → Writer → Critic → Formatter
        ↓
  Final Report (.md)
```

## Agents

| Agent | Role |
|---|---|
| **Researcher** | Searches web and gathers information |
| **Writer** | Transforms research into a structured report |
| **Critic** | Fact-checks and improves the report |
| **Formatter** | Creates the final polished markdown document |

## Tech Stack

| Layer | Tool |
|---|---|
| Agent Framework | CrewAI |
| LLM | Groq (Mixtral — Free!) |
| Web Search | Serper API (Free!) |
| Backend | FastAPI |
| Database | SQLite + SQLAlchemy |
| Dashboard | Streamlit |
| Deployment | Docker + Render |

## Quick Start (Local)

### 1. Clone & setup
```bash
git clone https://github.com/yourusername/multi-agent-system.git
cd multi-agent-system
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2. Add API keys
```bash
cp .env.example .env
# Edit .env with your keys
```

Free API keys:
- **Groq** → https://console.groq.com
- **Serper** → https://serper.dev

### 3. Run locally
```bash
# Terminal 1 - API
uvicorn api.main:app --reload

# Terminal 2 - Dashboard
streamlit run dashboard/app.py
```

- API: http://localhost:8000/docs
- Dashboard: http://localhost:8501

## Run with Docker

```bash
docker-compose up --build
```

## Deploy to Render

1. Push to GitHub
2. Go to https://render.com → New → Blueprint
3. Connect your repo
4. Add env vars: `GROQ_API_KEY`, `SERPER_API_KEY`
5. Deploy!

## Project Structure

```
multi-agent-system/
├── agents/          # Researcher, Writer, Critic, Formatter
├── tools/           # SearchTool, ScraperTool, MemoryTool
├── crew/            # Pipeline orchestration & tasks
├── api/             # FastAPI backend
├── db/              # SQLAlchemy models & CRUD
├── dashboard/       # Streamlit UI
├── config/          # Settings & env vars
├── Dockerfile
├── docker-compose.yml
├── render.yaml
└── main.py          # CLI entry point
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/jobs` | Start a research job |
| GET | `/api/jobs/{id}` | Get job status & report |
| GET | `/api/jobs` | List all jobs |
| DELETE | `/api/jobs/{id}` | Delete a job |

---
