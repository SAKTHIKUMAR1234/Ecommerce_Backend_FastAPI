from models.BaseModel import BaseModel

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Double
from sqlalchemy.orm import relationship

class ProductsModel(BaseModel):
  
  __tablename__ = 'products_table'
  
  product_name = Column(String(256),nullable=False)
  product_count = Column(Integer,nullable=False)
  product_price = Column(Double,nullable=False)
  vendor_id = Column(Integer,ForeignKey('vendor_table.id'),nullable=False)
  category_id = Column(Integer,ForeignKey('category_table.id'),nullable=False)
  
  vendor = relationship('VendorModel',back_populates='products')
  category = relationship('CategoryModel',back_populates='products')
  