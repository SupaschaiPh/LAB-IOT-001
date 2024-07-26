from sqlalchemy import  Column, Integer, String ,Date,Boolean , Float, DateTime , ForeignKey 
from sqlalchemy.orm import relationship , Mapped , mapped_column 
# from sqlalchemy.orm import relationship
from typing import List
import pytz


from database import Base
import datetime

bkk_timezone = pytz.timezone('Asia/Bangkok')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    stu_id = Column(Integer,index=True,unique=True,nullable=False)
    name = Column(String)
    lastname = Column(String)
    bod = Column(Date)
    gender = Column(String)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)
    cover_url = Column(String, nullable=True , default=None)
    category = Column(String)  # New field for book category
    description = Column(String)  # New field for book description
    synopsis = Column(String) 


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False , index=True)
    description = Column(String)
    price = Column(Float, nullable=False)
    cover_url = Column(String , nullable=True , default=None)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    #order_number = Column(String, unique=True, nullable=False, default=datetime.datetime.now(tz=bkk_timezone))
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(tz=bkk_timezone))
    updated_at = Column(DateTime,default=datetime.datetime.now(tz=bkk_timezone), onupdate=datetime.datetime.now(tz=bkk_timezone))
    note = Column(String,default=None, nullable=True)
    order_items:Mapped[List["OrderItem"]]  = relationship(back_populates="order",lazy='joined', cascade="all, delete")
    #order_items:Mapped["OrderItem"] = relationship("OrderItem", back_populates="order_id")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column( ForeignKey("orders.id") )
    menu_id = Column( ForeignKey("menu.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="order_items" , cascade="all, delete")
    menu : Mapped["Menu"]= relationship("Menu", backref="order_items",lazy='joined')
