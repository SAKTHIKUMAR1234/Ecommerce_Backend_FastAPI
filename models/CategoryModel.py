from models.BaseModel import BaseModel
from sqlalchemy import Column,Double,Integer,ForeignKey,String,Text
from sqlalchemy.orm import relationship

class CategoryModel(BaseModel):
  
  __tablename__ = 'category_table'

  category_name = Column(String(256),nullable=False,unique=True)
  category_description = Column(Text,nullable=False)
  
  products = relationship('ProductsModel',uselist=True,back_populates='category')