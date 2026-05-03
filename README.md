# Production GenAI Chatbot

A production-ready AI chatbot built with FastAPI, LangGraph, and Groq, designed for scalability, observability, and real-world deployment.

---

##  Features

* FastAPI backend (async, scalable)
* LangGraph agent workflow
* Groq LLM integration (low latency)
* JWT authentication (multi-user)
* Redis (session memory)
* PostgreSQL (chat history)
* Docker + Kubernetes ready
* CI pipeline with GitHub Actions
* Observability (logging, tracing ready)

---

##  Architecture

```
Client → FastAPI → LangGraph → LLM (Groq)
                ↓
        Redis (cache)
                ↓
      PostgreSQL (history)
```

---

## Setup

### 1. Create environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create `.env`:

```
POSTGRES_URL=postgresql+asyncpg://user:password@localhost:5432/chatdb
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_groq_api_key
SECRET_KEY=your_secret
```

---

##  Run with Docker

```bash
docker run -d -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=chatdb postgres
docker run -d -p 6379:6379 redis
```

---

##  Run Application

```bash
uvicorn app.main:app --reload
```

---

##  API Endpoints

* `POST /login` → get JWT token
* `POST /chat` → chatbot interaction
* `GET /history` → chat history
* `GET /health` → health check

---

##  Testing

```bash
python -m pytest
```

---

##  CI/CD

* GitHub Actions runs tests on every push
* Docker + Kubernetes ready for deployment

---

##  Notes

* JWT used for authentication
* Redis handles short-term memory
* PostgreSQL is the source of truth
* Designed for horizontal scaling

---

##  Future Improvements

* Refresh tokens
* Rate limiting
* Role-based access
* Monitoring dashboards

---
