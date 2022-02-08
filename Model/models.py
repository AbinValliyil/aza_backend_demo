from enum import unique
from importlib.resources import Package
from DB.database import Base
from sqlalchemy import String,Boolean,Integer,Column,DateTime,ForeignKey
# from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from typing import Text
# from sqlalchemy.utils.type import ChoiceType
from sqlalchemy.orm import  relationship



class AZAUser(Base):
    __tablename__='users'
    id            = Column(Integer,primary_key=True,autoincrement=True)
    name          = Column(String,nullable=False)
    mobile_number = Column(String,nullable=False,unique=True)
    password      = Column(String,nullable=False)
    created_at    = Column(DateTime, default=current_timestamp())
    updated_at    = Column(DateTime, onupdate=current_timestamp())
    #picks         = relationship('AZAPickup',back_populates='owner_pickup')
    
    #=relationship('AZADelivery',back_populates='delivery')
    # created_at    = Column(TIMESTAMP(timezone=True),nullable=False,server_default=Text('now()'))
    # packages=relationship('AZAPackage',back_populates='users_id')




