from models.BaseModel import BaseModel
from sqlalchemy import Column,Double,Integer,ForeignKey
from sqlalchemy.orm import relationship

class CartModel(BaseModel):
  
  __tablename__ = 'cart_table'
  
  user_id = Column(Integer,ForeignKey('user_table.id'),nullable=False,unique=True)
  
  user = relationship('UsersModel',uselist=False,back_populates='user_cart')
  cart_product_list = relationship('ProductCartModel',uselist=True,back_populates='cart')
  
  
class ProductCartModel(BaseModel):
  
  __tablename__ = 'product_cart_table'
  
  cart_id = Column(Integer, ForeignKey('cart_table.id'),nullable=False)
  product_id = Column(Integer, ForeignKey('products_table.id'),nullable=False)
  quantity = Column(Integer,default=1)
  
  product = relationship('ProductsModel',uselist=False)
  cart = relationship('CartModel',uselist=False,back_populates='cart_product_list')
  
  