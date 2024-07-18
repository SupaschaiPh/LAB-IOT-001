from sqlalchemy import  Column, Integer, String ,Date,Boolean
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

