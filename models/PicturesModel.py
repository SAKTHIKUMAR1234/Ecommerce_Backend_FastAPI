from models.BaseModel import BaseModel
from sqlalchemy import ForeignKey, String, Column, Text, Integer
from sqlalchemy.orm import relationship


class PictureModel(BaseModel):
  
  __tablename__ = 'picture_table'
  
  picture_url = Column(Text)
  picture_original_name = Column(Text)
  product_id = Column(Integer,ForeignKey('products_table.id'),nullable=False)
  
  product = relationship('ProductsModel',uselist=False,back_populates='product_images')