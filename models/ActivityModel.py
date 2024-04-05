from models.BaseModel import BaseModel

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship


class ActivityModel(BaseModel):
    
    __tablename__ = 'user_activity_table'
    
    user_id = Column(Integer,ForeignKey('user_table.id'),nullable=False)
    login_at = Column(DateTime(timezone=True),default=func.now())
    logout_at = Column(DateTime(timezone=True))
    session_id = Column(String(50),nullable=False)
    
    user = relationship('UsersModel', back_populates='activities')