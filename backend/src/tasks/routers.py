from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.user.controllers import get_current_user
from src.user.models import UserModel
from src.utils.db import get_db

task_routes = APIRouter(prefix="/tasks", tags=["tasks"])


@task_routes.post("/create", status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return controller.create_task(body, db, current_user.id)


@task_routes.get("/all_task", status_code=status.HTTP_200_OK)
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return controller.get_tasks(db, current_user.id)


@task_routes.get("/getby_id/{task_id}", status_code=status.HTTP_200_OK)
def get_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return controller.get_task_by_id(db, task_id, current_user.id)


@task_routes.put("/update/{task_id}", status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    body: TaskSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return controller.update_task(task_id, body, db, current_user.id)


@task_routes.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    controller.delete_task(task_id, db, current_user.id)
