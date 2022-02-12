from telnetlib import STATUS
from fastapi import APIRouter,Depends
from Model import schemas,models
from sqlalchemy.orm import session
from Security.jwt_bearer import JWTBearer
from DB.database import get_db ,SessionLocal
from uuid import uuid4


router = APIRouter()
db = SessionLocal()



@router.post('/Create_Order',dependencies=[Depends(JWTBearer())],tags=['Order For Shipind'])
def create_user_Order( package: schemas.Package_Create,Pickup_address:schemas.Pickup_Address_Create,Delivery_address:schemas.Delivery_Address_Create,Delivery_details:schemas.Delivery_Details_Create, user_id:str,db: session = Depends(get_db)):
    db_Package = models.Package(**package.dict(), owner_id=user_id)
    db.add(db_Package)
    db.commit()
    db.refresh(db_Package)
    db_Pickup_Address= models.Pickup_Address(**Pickup_address.dict(), owner_id=user_id)
    db.add( db_Pickup_Address)
    db.commit()
    db.refresh(db_Pickup_Address)
    db_Delivery_address= models.Delivery_Address(**Delivery_address.dict(), owner_id=user_id)
    db.add( db_Delivery_address)
    db.commit()
    db.refresh( db_Delivery_address)
    db_Delivery_details= models.Delivery_Details(**Delivery_details.dict(), owner_id=user_id)
    db.add(db_Delivery_details)
    db.commit()
    db.refresh(db_Delivery_details)
    return  str(uuid4())+'->'+str(user_id) + ','+"AZA"



@router.get('/Get_Order{user_id}',dependencies=[Depends(JWTBearer())],tags=['Get_All_Order'])
def get_an_order(user_id:str):

    package1 = db.query(models.Package).filter(models.Package.owner_id == user_id).all()
    package2 = db.query(models.Pickup_Address).filter(models.Pickup_Address.owner_id == user_id).all()
    package3 = db.query(models.Delivery_Address).filter(models.Delivery_Address.owner_id == user_id).all()
    package4 = db.query(models.Delivery_Details).filter(models.Delivery_Details.owner_id == user_id).all()
    return {'Package':package1 ,'Pickup_Address':package2,'Delivery_Address':package3,'Delivery_Details':package4}

