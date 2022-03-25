from typing_extensions import Self
from fastapi import APIRouter,Depends
from Model import schemas,models
from Security.jwt_bearer import JWTBearer
from DB.database import get_db ,SessionLocal
from uuid import uuid4
from sqlalchemy.orm import session

router = APIRouter()
db = SessionLocal()



@router.post('/Create_Order',tags=['USER_ORDER'])
def create_user_Order( package: schemas.Package_Create,Pickup_address:schemas.Pickup_Address_Create,Delivery_address:schemas.Delivery_Address_Create,Delivery_details:schemas.Delivery_Details_Create, user_id:str,db: session = Depends(get_db)):
    try:
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
    except:
           return {"status":404}
    return  {'id':str(uuid4())+'->'+str(user_id) + ','+"AZA",'status':200}
   


@router.get('/get_userorder',dependencies=[Depends(JWTBearer())],tags=['USER_ORDER'])
def get_an_order(user_id:str):

   
    package = db.query(models.Pickup_Address).filter(models.Pickup_Address.owner_id == user_id).first()

    return {'Pickup_Address':package}


