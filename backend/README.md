# TaskFlow — Task Management API

A small, production-shaped task management backend: FastAPI + SQLAlchemy + PostgreSQL,
with JWT authentication and per-user task ownership. Includes a minimal static
frontend for exercising the API by hand, a Dockerfile/compose setup, and a
pytest suite that runs against SQLite (no Postgres needed to run the tests).

## Features

- **Auth:** register / login with hashed passwords (Argon2 via `pwdlib`) and JWT access tokens.
- **Tasks:** create, list, get, update, delete — each task belongs to exactly one user,
  and users can only see or modify their own tasks.
- **Validation:** Pydantic v2 schemas for every request/response body.
- **CORS:** configurable via `ALLOWED_ORIGINS`.
- **Tests:** `pytest` suite covering auth, CRUD, and cross-user task isolation.

## Project structure

```
Complete-TaskManager/
├── src/
│   ├── main.py              # FastAPI app, CORS, table creation
│   ├── requirements.txt
│   ├── tasks/                # task CRUD (models, schemas, controller, routes)
│   ├── user/                 # auth: register/login/me (models, schemas, controller, routes)
│   └── utils/                # settings, DB session
├── tests/                    # pytest suite (uses SQLite)
├── static-demo/index.html    # single-file demo frontend (vanilla JS, no build step)
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Getting started (local)

1. **Create and fill in your `.env`** (never commit the real one — it's already gitignored):

   ```bash
   cp .env.example .env
   # then edit .env: set DB_CONNECTION to a real Postgres URL and SECRET_KEY to a random string
   ```

2. **Install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r src/requirements.txt
   ```

3. **Run the API** (tables are created automatically on startup):

   ```bash
   uvicorn src.main:app --reload
   ```

   Interactive docs: `http://localhost:8000/docs`

4. **Frontend:** the real frontend is the React app in `../frontend` (see its own
   README). `static-demo/index.html` is a zero-build vanilla-JS page kept around
   for quick manual testing — just open it in a browser and point it at your API's
   base URL.

## Running with Docker

```bash
docker compose up --build
```

This starts Postgres and the API together. The API will be on `http://localhost:8000`.
Set a real `SECRET_KEY` env var before running in anything beyond local testing.

## Running tests

Tests run against a throwaway SQLite file, so no database setup is required:

```bash
pip install -r src/requirements.txt
pytest tests/ -v
```

## API overview

| Method | Path                     | Auth required | Description                  |
|--------|--------------------------|:-:|-------------------------------|
| POST   | `/user/register`         |   | Create an account             |
| POST   | `/user/login`            |   | Get a JWT access token        |
| GET    | `/user/me`                | ✓ | Current user's profile        |
| POST   | `/tasks/create`          | ✓ | Create a task                 |
| GET    | `/tasks/all_task`        | ✓ | List your tasks               |
| GET    | `/tasks/getby_id/{id}`   | ✓ | Get one of your tasks         |
| PUT    | `/tasks/update/{id}`     | ✓ | Update one of your tasks      |
| DELETE | `/tasks/delete/{id}`     | ✓ | Delete one of your tasks      |

Authenticated requests need `Authorization: Bearer <token>`.

## What was fixed/added on top of the original scaffold

- Task routes had no auth dependency at all and tasks had no owner — anyone could
  read/edit/delete anyone's tasks. Added a `get_current_user` dependency and a
  `user_id` foreign key on tasks; every task endpoint is now scoped to the caller.
- `user/controllers.py` referenced the `Settings` **class** instead of the `settings`
  **instance**, and `jwt.decode(...)` passed the algorithm as a bare string instead of
  `algorithms=[...]` — both would have raised errors at runtime. Fixed, plus proper
  401 handling for expired/invalid tokens.
- A typo (`HTTP_401_UNAUTHORIZEDt`) would have crashed on any auth failure. Fixed.
- `requirements.txt` was empty. Filled in with pinned versions.
- Delete endpoint declared `204 No Content` but returned a JSON body, which is invalid.
  It now returns nothing, as `204` requires.
- Added response models (`from_attributes=True`) so API responses have a stable shape.
- Added `.env.example`, a `Dockerfile` + `docker-compose.yml`, a pytest suite, and the
  `static-demo/index.html` demo page, none of which existed before.
