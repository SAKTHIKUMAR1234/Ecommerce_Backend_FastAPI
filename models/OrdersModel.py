from models.BaseModel import BaseModel

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class OrdersModel(BaseModel):
  
  __tablename__ = 'orders_table'
  
  user_id = Column(Integer,ForeignKey('user_table.id'),nullable=False)
  razor_pay_order_id = Column(String(50),nullable=True,default=None)
  
  payment = relationship('PaymentModel',uselist=False,back_populates='order')
  ordered_items = relationship('OrderItemModel',uselist=True,back_populates='order')
  user = relationship('UsersModel',uselist=False,backref='orders')
  
  
class OrderItemModel(BaseModel):
  
  __tablename__ = 'order_item_table'
  
  order_id = Column(Integer,ForeignKey('orders_table.id'),nullable=False)
  product_id = Column(Integer, ForeignKey('products_table.id'),nullable=False)
  quantity = Column(Integer,default=1)
  
  product = relationship('ProductsModel',uselist=False)
  order = relationship('OrdersModel',uselist=False,back_populates='ordered_items')