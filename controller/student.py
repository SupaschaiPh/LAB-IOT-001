from database import   get_db
from fastapi import Depends, Response, APIRouter, Body 
import models
from sqlalchemy.orm import Session

from typeDTO import UserDTO,UserEditDTO

from typing import Annotated



## USSERRRRRR
router_v1 = APIRouter(prefix='/api/v1/student')

@router_v1.get('/')
async def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router_v1.get('/{stu_id}')
async def get_user(stu_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.stu_id == stu_id).first()


@router_v1.post('/')
async def create_user(user: Annotated[UserDTO, Body()], response: Response, db: Session = Depends(get_db)):
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

@router_v1.patch('/{stu_id}')
async def update_user(stu_id: int,response: Response , user: Annotated[UserEditDTO, Body()], db: Session = Depends(get_db)):
    try:
        #existing_user = models.User(
        #    stu_id=user.stu_id,
        #    name=user.name, lastname=user.lastname, bod=user.bod, gender=user.gender)
        existing_user = db.query(models.User).filter(models.User.stu_id == stu_id).first()
        if not existing_user:
            response.status_code = 404
            return {"message": "Book not found"}
        for key, value in user.dict().items():
            if not value is  None:
                setattr(existing_user, key, value)
        db.commit()
        db.refresh(existing_user)
        return existing_user
    except:
        db.rollback()
        response.status_code = 500
        return {
        "messgage": "update fail",
             "help":"pls check date string is correct or stu_id have already been in database"
        }


@router_v1.delete('/{stu_id}')
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
