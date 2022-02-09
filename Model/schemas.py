from lib2to3.pgen2 import token
from os import access
from pydantic import BaseModel
from datetime  import datetime
from fastapi import Body
from typing import List,Optional



class AZA_SingUp(BaseModel):
    name:str
    mobile_number:str
    password:str
class AZAUser_res(BaseModel):
    id             :int
    name           :str
    mobile_number  :int
    
    
    class Config:
         orm_mode = True



class AZAUser_login(BaseModel):

    mobile_number  :str
    password       :str



class AZAUser_login_res(BaseModel):


    id             :int
    mobile_number  :int
   
   
    class config:
        orm_mode = True


class Token(BaseModel):
    token :str




class AZA_geocode(BaseModel):
    pin1:str
    pin2:str
    
