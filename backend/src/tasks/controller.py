from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.tasks.dtos import TaskSchema
from src.tasks.models import TaskModel


def create_task(body: TaskSchema, db: Session, user_id: int):
    new_task = TaskModel(
        title=body.title,
        description=body.description,
        is_completed=body.is_completed,
        user_id=user_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "data": new_task,
    }


def get_tasks(db: Session, user_id: int):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id).all()
    return {"tasks": tasks}


def _get_owned_task_or_404(db: Session, task_id: int, user_id: int) -> TaskModel:
    task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id, TaskModel.user_id == user_id)
        .first()
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


def get_task_by_id(db: Session, task_id: int, user_id: int):
    return _get_owned_task_or_404(db, task_id, user_id)


def update_task(task_id: int, body: TaskSchema, db: Session, user_id: int):
    task = _get_owned_task_or_404(db, task_id, user_id)

    task.title = body.title
    task.description = body.description
    task.is_completed = body.is_completed

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated successfully",
        "data": task,
    }


def delete_task(task_id: int, db: Session, user_id: int):
    task = _get_owned_task_or_404(db, task_id, user_id)

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
