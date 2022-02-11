from pydantic import BaseModel
from datetime  import datetime
from fastapi import Body
from typing import List,Optional

#signup model

class AZA_SingUp(BaseModel):
    name           :str
    mobile_number  :str
    password       :str


class AZAUser_res(BaseModel):
    id             :int
    name           :str
    mobile_number  :int
    
    class Config:
         orm_mode = True



# login model


class AZAUser_login(BaseModel):

    mobile_number:str
    password     :str

class AZAUser_login_res(BaseModel):


    id           :int
    mobile_number:int
   
    class config:
        orm_mode = True



# Zipcode model

class AZA_geocode(BaseModel):
    pin1      :str
    pin2      :str



    
#package model

class PackageBase(BaseModel):
 package_size       :str
 package_type       :str
 package_price      :int


class Package_Create(PackageBase):
    pass


class Pack(PackageBase):
    id             :int
    owner_id       :int
     
    class Config:
        orm_mode = True



# pickup model

class PICKUPBase(BaseModel):
    name          :str
    mobile_number :str
    building_no   :int
    area          :str
    city          :str
    state         :str
    pincode       :int
    

class Pickup_Address_Create(PICKUPBase):
    pass


class PICKUP(PICKUPBase):
    id          : int
    owner_id    : int

    class Config:
        orm_mode = True

# delivery model 

class DELIVERYBase(BaseModel):
    name          :str
    mobile_number :str
    building_no   :int
    area          :str
    city          :str
    state         :str
    pincode       :int

class  Delivery_Address_Create( DELIVERYBase):
    pass


class DD( DELIVERYBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# delivery details model

class Delivery_Details(BaseModel):
 delivery_status :str
 delivery_time   :str
 delivery_type   :str
 pickup_date     :str 


class Delivery_Details_Create(Delivery_Details):
    pass


class Delivery_Details_id(Delivery_Details):
    id         : int
    owner_id   : int

    class Config:
        orm_mode = True