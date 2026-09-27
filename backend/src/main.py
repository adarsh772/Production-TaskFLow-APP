from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.tasks.models import TaskModel  # noqa: F401 (registers table with Base)
from src.tasks.routers import task_routes
from src.user.models import UserModel  # noqa: F401 (registers table with Base)
from src.user.router import user_routes
from src.utils.db import Base, engine
from src.utils.settings import settings

Base.metadata.create_all(engine)

app = FastAPI(
    title="TaskFlow API",
    description="A production-ready task management API with JWT authentication.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_routes)
app.include_router(user_routes)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "TaskFlow API"}
