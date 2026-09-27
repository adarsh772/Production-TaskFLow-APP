# TaskFlow

A full-stack task manager: FastAPI + PostgreSQL backend with JWT auth and
per-user task ownership, and a React (Vite) frontend.

```
TaskFlow/
├── backend/    # FastAPI API — see backend/README.md
├── frontend/   # React (Vite) app — see frontend/README.md
└── docker-compose.yml   # runs db + api + web together
```

## Quickest start: Docker Compose

From the repo root:

```bash
docker compose up --build
```

- API: `http://localhost:8000` (docs at `/docs`)
- Frontend: `http://localhost:5173`
- Postgres: `localhost:5432` (user/pass `postgres`, db `taskflow_db`)

Set a real `SECRET_KEY` env var before using this beyond local testing:

```bash
SECRET_KEY=$(openssl rand -hex 32) docker compose up --build
```

## Running without Docker

Each half has its own setup instructions:

- **[backend/README.md](backend/README.md)** — Python env, `.env`, `uvicorn`, tests.
- **[frontend/README.md](frontend/README.md)** — `npm install`, `.env`, `npm run dev`.

Short version:

```bash
# backend
cd backend
cp .env.example .env   # point DB_CONNECTION at a real Postgres instance
python -m venv venv && source venv/bin/activate
pip install -r src/requirements.txt
uvicorn src.main:app --reload

# frontend (separate terminal)
cd frontend
cp .env.example .env   # VITE_API_BASE_URL=http://localhost:8000
npm install
npm run dev
```

Make sure the backend's `ALLOWED_ORIGINS` includes wherever the frontend is
served from (`http://localhost:5173` for the Vite dev server).

## What's inside

- **Auth:** register / login, Argon2-hashed passwords, JWT access tokens.
- **Tasks:** create / list / update / delete, scoped to the logged-in user —
  enforced server-side, not just hidden in the UI.
- **Tests:** `backend/tests` (pytest, runs against SQLite, no Postgres needed).
- **backend/static-demo/index.html:** a zero-build vanilla-JS page for quick
  manual API testing, independent of the React app.
