from models.BaseModel import BaseModel

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Float, Text
from sqlalchemy.orm import relationship
from enum import Enum as pyenum

class VendorStatus(pyenum):
  
  accepted = 0
  rejected = 1
  pending = 2
  
  
class VendorModel(BaseModel):
  
  __tablename__ = 'vendor_table'
  
  vendor_name = Column(String(256),nullable=False,unique=True)
  vendor_address = Column(Text,nullable=False)
  user_id = Column(Integer,ForeignKey('user_table.id'),nullable=False)
  status = Column(Integer,default=VendorStatus.pending.value)
  
  products = relationship('ProductsModel',uselist=True,back_populates='vendor')
  user = relationship('UsersModel')