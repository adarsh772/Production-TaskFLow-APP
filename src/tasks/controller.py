from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException


def create_task(body: TaskSchema, db: Session):
    data = body.model_dump()

    new_task = TaskModel(
        title=data["title"],
        discription=data["discription"],
        is_completed=data["is_completed"]
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "data": new_task
    }


def get_task(db: Session):
    tasks = db.query(TaskModel).all()

    return {
        "tasks": tasks
    }


def get_tasks_byid(db: Session, task_id: int):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


def update_task(task_id: int, body: TaskSchema, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = body.title
    task.discription = body.discription
    task.is_completed = body.is_completed

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated successfully",
        "data": task
    }


def delete_task(task_id: int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }