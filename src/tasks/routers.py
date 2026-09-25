from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db


task_routes=APIRouter(prefix="/tasks")

@task_routes.post("/create",status_code=status.HTTP_201_CREATED)
def create_task(body: TaskSchema, db=Depends(get_db)):
    return controller.create_task(body, db)


@task_routes.get("/all_task",status_code=status.HTTP_200_OK)
def get_all_tasks(db=Depends(get_db)):
    return controller.get_task(db)


@task_routes.get("/getby_id/{task_id}",status_code=status.HTTP_200_OK)
def get_by_id(task_id: int, db: Session = Depends(get_db)):
    return controller.get_tasks_byid(db, task_id)


@task_routes.put("/update/{task_id}",status_code=status.HTTP_201_CREATED)
def update_task(
    task_id: int,
    body: TaskSchema,
    db: Session = Depends(get_db)
):
    return controller.update_task(task_id, body, db)


@task_routes.delete("/delete/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def deletetask(task_id: int, db: Session = Depends(get_db)):
    return controller.delete_task(task_id, db)