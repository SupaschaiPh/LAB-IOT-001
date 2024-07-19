from database import   get_db
from fastapi import Depends, Response, APIRouter, Body 
import models
from sqlalchemy.orm import Session

from typeDTO import BookDTO,BookEditDTO

from typing import Annotated

router_v1 = APIRouter(prefix='/api/v1')


@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int,response: Response , db: Session = Depends(get_db)):
    res = db.query(models.Book).filter(models.Book.id == book_id).first()
    if res:
        return res
    response.status_code = 404
    return res

@router_v1.post('/books')
async def create_book(book:Annotated[BookDTO,Body()], response: Response , db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book.title, author=book.author, year=book.year, is_published=book.is_published,description=book.description,category=book.category,synopsis=book.synopsis , cover_url = book.cover_url)
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: Annotated[BookEditDTO,Body()] ,response: Response , db: Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing_book:
        response.status_code = 404
        return {"message": "Book not found"}

    for key, value in book.dict().items():
        if not value is  None:
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
