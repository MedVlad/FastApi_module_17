from typing import Annotated

from fastapi.params import Path
from pydantic import BaseModel

class CreateTask(BaseModel):
    name: str
    description : str
    price : int
    image_url: str
    stock : int
    category : int

class UpdateTask(BaseModel):
    name: str
    description : str
    price : int
    image_url: str
    stock : int
    category : int

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