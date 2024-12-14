from typing import Annotated, Optional

from fastapi.params import Path
from pydantic import BaseModel

class CreateTask(BaseModel):

    title : str
    content : str
    priority : int
    user_id : int
    completed : bool = False
    slug : str

class UpdateTask(BaseModel):
    id : int = None
    title : str
    content : str
    priority : int
    user_id : int
    completed : bool = None
    slug : str

class CreateUser(BaseModel):
    username : str
    firstname :str
    lastname : str
    age : int
    slug : str

class UpdateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int
    id : int=None