from models.BaseModel import BaseModel

from sqlalchemy import Column, String,Text,Boolean,Integer,ForeignKey,Enum
from sqlalchemy.orm import relationship
from enum import Enum as pyenum

class RoleEnum(pyenum):
  
  user = 0
  admin = 1
  dev = 2

class UsersModel(BaseModel):
  
  __tablename__ = 'user_table'
  
  first_name = Column(String(50),nullable=False)
  last_name = Column(String(50),nullable=False)
  email = Column(String(100),nullable=False)
  password = Column(Text,nullable=False)
  phone_number = Column(String(10),nullable=False)
  isdev = Column(Boolean,default=False)
  role = Column(Integer,default=RoleEnum.user.value)
  
  user_cart = relationship('CartModel',uselist=False,back_populates='user')
  activities = relationship('ActivityModel',uselist=True,back_populates='user')