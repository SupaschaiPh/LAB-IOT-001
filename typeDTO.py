from pydantic import BaseModel
from typing import List

class UserDTO(BaseModel):
    stu_id: int
    name: str
    lastname: str
    bod: str
    gender: str

class MenuDTO(BaseModel):
    name: str 
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

class OrderItemDTO(BaseModel):
    menu_id: int
    quantity: int

class OrderCreateDTO(BaseModel):
    order_items: List[OrderItemDTO]

class OrderResponseDTO(BaseModel):
    id: int
    order_number: str
    total_price: float
    created_at: str
    order_items: List[OrderItemDTO]
