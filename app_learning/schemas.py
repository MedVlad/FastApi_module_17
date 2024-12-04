from pydantic import BaseModel
from sqlalchemy import Boolean, Float


class CreateProduct(BaseModel):
    id : int
    name: str
    slug : str
    descriptioin : str
    price : int
    image_url: str
    stock : int
    category_id : int
    rating : Float
    is_active : Boolean


class CreateCategory(BaseModel):
    id:int
    name : str
    slug : str
    is_active:Boolean
    parent_id : int
