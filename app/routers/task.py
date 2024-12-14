from fastapi import APIRouter, Depends, status, HTTPException, Path
# Сессия БД
from sqlalchemy.orm import Session

# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.user import User
from app.models.task import Task
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify
from app.schemas import CreateTask, UpdateTask
router = APIRouter(prefix='/task', tags=["task"])

@router.get("/all_tasks")
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks_all = db.scalars(select(Task)).all()
    return tasks_all

@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(User).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no task found")
    return task

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    db.execute(insert(Task).values(user_id=create_task.user_id,
                                   title=create_task.title,
                                   completed=create_task.completed,
                                   slug=slugify(create_task.title),
                                   content=create_task.content,
                                   priority=create_task.priority))
    db.commit()
    return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"}

@router.put("/update_task")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    task_old = db.scalar(select(Task).where(Task.id == task_id))
    if task_old is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no user found")
    db.execute(update(Task).where(Task.id == task_id).values(
        user_id=task_old.user_id if update_task.user_id == "string" else update_task.user_id,
        title=task_old.title if update_task.title == "string" else update_task.title,
        completed=task_old.completed if update_task.completed is None else update_task.completed,
        content=task_old.content if update_task.content == "string" else update_task.content,
        priority=task_old.priority if update_task.priority == 0 else update_task.priority,
        slug=task_old.slug if update_task.slug == "string" else slugify(update_task.priorityslug)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': f'Task {task_old.title} update is successful!'
    }

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_del = db.scalar(select(Task).where(Task.id == task_id))
    if task_del is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no task found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': f'Task {task_del.title} delete is successful!'
    }