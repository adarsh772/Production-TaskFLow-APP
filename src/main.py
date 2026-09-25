from fastapi import FastAPI
from src.utils.db import engine,Base
from src.tasks.models import TaskModel
from src.tasks.routers import task_routes

Base.metadata.create_all(engine)

app=FastAPI(title="This is a Complete FAstAPI Application.")
app.include_router(task_routes)