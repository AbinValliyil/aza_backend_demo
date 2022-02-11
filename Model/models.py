from ast import Index
from enum import unique
from importlib.resources import Package
from DB.database import Base
from sqlalchemy import String,Boolean,Integer,Column,DateTime,ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from typing import Text
from sqlalchemy.orm import  relationship



class AZAUser(Base):
    __tablename__='users'
    id                = Column(Integer,primary_key=True,autoincrement=True)
    name              = Column(String,nullable=False)
    mobile_number     = Column(String,nullable=False,unique=True)
    password          = Column(String,nullable=False)
    created_at        = Column(DateTime, default=current_timestamp())
    updated_at        = Column(DateTime, onupdate=current_timestamp())
    package_details   = relationship("Package", back_populates="owner")
    pickup_address    = relationship("Pickup_Address", back_populates="owner")
    delivery_address  = relationship("Delivery_Address", back_populates="owner")
    delivery_details  = relationship("Delivery_Details", back_populates="owner")
  


class Package(Base):
    __tablename__ = "packages"

    id               = Column(Integer, primary_key=True)
    package_size     = Column(String, nullable=True)
    package_type     = Column(String, index=True)
    package_price    = Column(Integer, nullable=True)
    created_at       = Column(DateTime, default=current_timestamp())
    owner_id         = Column(Integer, ForeignKey("users.id"))
    owner            = relationship("AZAUser", back_populates="package_details")



class Pickup_Address(Base):
        
    __tablename__ = "pickup_address"

    id               = Column(Integer, primary_key=True)
    name             = Column(String, index=True)
    mobile_number    = Column(String,nullable=False)
    building_no      = Column(Integer, nullable=True)
    area             = Column(String, index=True)
    city             = Column(String, index=True)
    state            = Column(String, index=True)
    pincode          = Column(Integer, nullable=True)
    owner_id         = Column(Integer, ForeignKey("users.id"))
    owner            = relationship("AZAUser", back_populates="pickup_address")


class Delivery_Address(Base):
        
    __tablename__ = "delivery_address"

    id               = Column(Integer, primary_key=True)
    name             = Column(String, index=True)
    mobile_number    = Column(String,nullable=False)
    building_no      = Column(Integer, nullable=True)
    area             = Column(String, index=True)
    city             = Column(String, index=True)
    state            = Column(String, index=True)
    pincode          = Column(Integer, nullable=True)
    owner_id         = Column(Integer, ForeignKey("users.id"))
    owner            = relationship("AZAUser", back_populates="delivery_address")


class Delivery_Details(Base):
    __tablename__ ='delivery_details'

    id                = Column(Integer,primary_key=True)
    delivery_status   = Column(String,nullable=True)
    delivery_time     = Column(String,nullable=True)
    delivery_type     = Column(String,nullable=True)
    pickup_date       = Column(String,nullable=True)
    owner_id          = Column(Integer, ForeignKey("users.id"))
    owner             = relationship("AZAUser", back_populates="delivery_details")

