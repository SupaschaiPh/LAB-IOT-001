from sqlalchemy import  Column, Integer, String ,Date
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
