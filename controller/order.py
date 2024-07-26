from fastapi import APIRouter, Depends, Response,Body
from sqlalchemy.orm import Session

from database import get_db

from models import Order, OrderItem, Menu
from typeDTO import OrderDTO

from typing import Annotated



router_v1 = APIRouter(prefix='/api/v1')

@router_v1.get("/orders")
async def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

@router_v1.post("/orders")
async def create_order(order_data: Annotated[OrderDTO,Body()] , db: Session = Depends(get_db)):
    total_price = sum(item.quantity * menu.price for item in order_data.order_items for menu in db.query(Menu).filter_by(id=item.menu_id))
    order = Order(total_price=total_price,note=order_data.note)
    db.add(order)
    db.commit()
    db.refresh(order)

    order_items = []
    for item in order_data.order_items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        order_item = OrderItem(order_id=order.id, menu_id=item.menu_id, quantity=item.quantity, price=menu.price)
        order_items.append(order_item)
        db.add(order_item)
    db.commit()
    db.refresh(order)

    return order

@router_v1.get("/orders/{order_id}")
async def get_order(order_id: int ,response: Response, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        response.status_code = 404
        return {"message": "Order not found"}
    return order

@router_v1.patch("/orders/{order_id}")
async def update_order(order_id: int, order_data: Annotated[OrderDTO,Body()] ,response: Response , db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        response.status_code = 404
        return {"message": "Order not found"}
    if "note" in order_data.dict(exclude_unset=True):
        order.note = order_data.note
    order.total_price = sum(item.quantity * menu.price for item in order_data.order_items for menu in db.query(Menu).filter_by(id=item.menu_id))

    for item in order_data.order_items:
        order_item = db.query(OrderItem).filter(OrderItem.order_id == order_id and OrderItem.menu_id == item.menu_id).first()
        if order_item:
            menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
            order_item.quantity = item.quantity
            order_item.price = menu.price  
    db.commit()
    db.refresh(order)
    return order

@router_v1.delete("/orders/{order_id}")
async def delete_order(order_id: int ,response: Response, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        response.status_code = 404
        return {"message": "Order not found"}

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
