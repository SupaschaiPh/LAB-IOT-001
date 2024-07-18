from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from fastapi import FastAPI, Depends, Response, APIRouter, Body, File , UploadFile
from fastapi.responses import RedirectResponse
import models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
from pydantic import BaseModel
from typing import Annotated

import os

# For Validation


# Import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserModelDTO(BaseModel):
    stu_id: int
    name: str
    lastname: str
    bod: str
    gender: str

class MenuSchema(BaseModel):
    name: str 
    description: str 
    price: float 

#class EditUserModelDTO(BaseModel):
#    stu_id: int | None
#    name: str | None = None
#    lastname: str | None = None
#    bod: str | None = None
#    gender: str | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url='/docs')

## Book

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, cover: UploadFile , db: Session = Depends(get_db)):
    if cover :
        print(cover.filename)
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'],description=book['description'],category=book['category'],synopsis=book['synopsis'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict ,response: Response , db: Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing_book:
        response.status_code = 404
        return {"message": "Book not found"}

    for key, value in book.items():
        setattr(existing_book, key, value)

    db.commit()
    db.refresh(existing_book)
    return existing_book

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int,response: Response, db: Session = Depends(get_db)):
    book_to_delete = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book_to_delete:
        response.status_code = 404
        return {"message": "Book not found"}

    db.delete(book_to_delete)
    db.commit()
    return {"detail": "Book deleted successfully"}

## USSERRRRRR

@router_v1.get('/users')
async def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router_v1.get('/users/{stu_id}')
async def get_user(stu_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.stu_id == stu_id).first()


@router_v1.post('/users')
async def create_user(user: Annotated[UserModelDTO, Body()], response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    try:
        newUser = models.User(
            stu_id=user.stu_id,
            name=user.name, lastname=user.lastname, bod=user.bod, gender=user.gender)
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        response.status_code = 201
        return newUser
    except:
        db.rollback()
        response.status_code = 500
        return {
            "message":"server error",
            "help":"pls check date string is correct or stu_id have already been in database"
        }

@router_v1.patch('/users/{stu_id}')
async def update_user(stu_id: int,response: Response , user: Annotated[UserModelDTO, Body()], db: Session = Depends(get_db)):
    try:
        newUser = models.User(
            stu_id=user.stu_id,
            name=user.name, lastname=user.lastname, bod=user.bod, gender=user.gender)
        infected = db.query(models.User).filter(models.User.stu_id == stu_id).update(
            {
                models.User.stu_id: newUser.stu_id,
                models.User.name: newUser.name,
                models.User.lastname: newUser.lastname,
                models.User.bod: newUser.bod,
                models.User.gender: newUser.gender,

            }
        )

        db.commit()
        if(infected == 0):
            response.status_code = 404
            return {
                "messgage":"May not found stu_id"
            }
        response.status_code = 201
        return {
            "messgage": "update success",
            "new":newUser,
        }
    except:
        db.rollback()
        response.status_code = 500
        return {
        "messgage": "update fail",
             "help":"pls check date string is correct or stu_id have already been in database"
        }


@router_v1.delete('/users/{stu_id}')
async def delete_user(stu_id: int , response: Response , db: Session = Depends(get_db)):
    try:
        infected = db.query(models.User).filter(models.User.stu_id ==stu_id).delete()
        db.commit()
        if(infected == 0):
            response.status_code = 404
            return {
                "messgage":"May not found stu_id"
            }
        return {
            "messgage": "delete success"
        }
    except:
        db.rollback()
        response.status_code = 500
        return {
        "messgage": "delete fail",
        "help":"pls stu_id is have been in database"
    }





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
async def create_menu(menu: MenuSchema, db: Session = Depends(get_db)):
    new_menu = Menu(
        name=menu.name,
        description=menu.description,
        price=menu.price,
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu






app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host=os.environ.get("HOST","127.0.0.1"))
