from models.BaseModel import BaseModel
from sqlalchemy import Column,Enum,func,String,Text,Double,Integer,ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as pyenum


class PaymentSatus(pyenum):
  
  completed = 'COMPLETED'
  pending = 'PENDING'
  failed = 'FAILED'
  
  
  
class PaymentModel(BaseModel):
  
    __tablename__ = 'payment_table'

    order_id = Column(Integer, ForeignKey('orders_table.id'))  
    payment_amount = Column(Double) 
    payment_method = Column(String(50))
    payment_status = Column(Enum(PaymentSatus),default=PaymentSatus.pending)
    transaction_id = Column(String(100))
    payment_details = Column(Text)
    
    order = relationship("OrdersModel", uselist=False, back_populates="payment")
    
