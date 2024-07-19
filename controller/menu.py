from database import   get_db
from fastapi import Depends, Response, APIRouter, Body 
import models
from sqlalchemy.orm import Session

from typeDTO import MenuDTO

from typing import Annotated

router_v1 = APIRouter(prefix='/api/v1')



@router_v1.get('/menus')
async def get_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()
    return menus
@router_v1.get('/menus/{menu_id}')
async def get_menu(menu_id: int , response: Response, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        response.status_code = 404
        return {"message": "Menu not found"}
    return menu
@router_v1.post('/menus')
async def create_menu(menu: Annotated[MenuDTO,Body()], db: Session = Depends(get_db)):
    new_menu = models.Menu(
        name=menu.name,
        description=menu.description,
        price=menu.price,
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

@router_v1.patch('/menus/{menu_id}')
async def update_menu(menu_id: int, updated_menu: Annotated[MenuDTO,Body()] ,response: Response, db: Session = Depends(get_db)):
    existing_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not existing_menu:
        response.status_code = 404
        return {"message": "Menu not found"}
    for key, value in updated_menu.dict(exclude_unset=True).items():
        setattr(existing_menu, key, value)

    db.commit()
    db.refresh(existing_menu)
    return existing_menu

@router_v1.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int, response: Response, db: Session = Depends(get_db)):
    menu_to_delete = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu_to_delete:
        response.status_code = 404
        return {"message": "Menu not found"}

    db.delete(menu_to_delete)
    db.commit()
    return {"detail": "Menu deleted successfully"}

