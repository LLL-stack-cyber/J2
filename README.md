# Jarvis AI Study Agent

Jarvis is a full-stack AI study platform with:
- FastAPI backend APIs
- Next.js frontend dashboard
- RAG-style notes retrieval for tutoring
- Quiz generation + exam analysis
- PostgreSQL-ready SQLAlchemy schema
- Docker deployment files

## Structure

```text
backend/
frontend/
services/
deploy/
```

## Quick Start (Run the App)

### Windows (Recommended)
Simply double-click `start.bat` to automatically install dependencies and start both frontend and backend.

### Python Wrapper
Run the following to start both services together:
```bash
python run_app.py
```

### Docker (Production-ready)
To run everything inside Docker containers:
```bash
python run_app.py --docker
```
or directly:
```bash
docker compose -f deploy/docker-compose.yml up --build
```

## Backend (FastAPI)
- **Host:** `http://localhost:8000`
- **Docs:** `http://localhost:8000/docs`

## Frontend (Next.js)
- **Host:** `http://localhost:3000`

## Core API routes
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/upload/notes`
- `POST /api/quiz/generate`
- `POST /api/mentor/chat`
- `POST /api/mentor/exam-analysis`

## Tests

```bash
pytest backend/tests -q
```

## Docker

```bash
cd deploy
docker compose up --build
```
