from sqlalchemy import  Column, Integer, String ,Date,Boolean , Float
# from sqlalchemy.orm import relationship

from database import Base

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
    cover_url = Column(String)
    category = Column(String)  # New field for book category
    description = Column(String)  # New field for book description
    synopsis = Column(String) 


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
