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

router = APIRouter(prefix='/user', tags=["user"])


@router.get("/all_users")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    users_all = db.scalars(select(User)).all()
    return users_all

@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if tasks.__len__() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no tasks found")
    return tasks

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no user found")
    return user


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {"status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"}


@router.put("/update_user")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user_old = db.scalar(select(User).where(User.id == user_id))
    if user_old is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no user found")
    db.execute(update(User).where(User.id == user_id).values(
        username=user_old.username if update_user.username == "string" else update_user.username,
        firstname=user_old.firstname if update_user.firstname == "string" else update_user.firstname,
        lastname=user_old.lastname if update_user.lastname == "string" else update_user.lastname,
        age=user_old.age if update_user.age == 0 else update_user.age))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': f'User {user_old.username} update is successful!'
    }


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_del = db.scalar(select(User).where(User.id == user_id))
    if user_del is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no user found")
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': f'User {user_del.username} deleted is successful!'
    }
