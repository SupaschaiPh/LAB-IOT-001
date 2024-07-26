from pydantic import BaseModel,Field
from typing import List
import datetime


class UserDTO(BaseModel):
    stu_id: int
    name: str
    lastname: str
    bod: datetime.date|datetime.datetime
    gender: str

class UserEditDTO(BaseModel):
    stu_id: int|None = None
    name: str|None = None
    lastname: str|None = None
    bod: datetime.date|datetime.datetime|None = None
    gender: str|None = None

class MenuDTO(BaseModel):
    name: str 
    cover_url: str|None = None
    description: str  = ""
    price: float 

class BookDTO(BaseModel):
    title: str
    description: str = ""
    author: str
    year: int = 2024
    is_published: bool = True
    cover_url: str = ""
    category: str = ""
    synopsis: str = ""

class BookEditDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
    year: int | None = None
    is_published: bool | None = None
    cover_url: str | None = None
    category: str | None = None
    synopsis: str | None = None

class OrderItemDTO(BaseModel):
    menu_id: int 
    quantity: int

class OrderDTO(BaseModel):
    order_items: List[OrderItemDTO] = Field(min_items=1)
    note:str|None = None

class OrderResponseDTO(BaseModel):
    id: int
    order_number: str
    total_price: float
    created_at: str
    order_items: List[OrderItemDTO]
