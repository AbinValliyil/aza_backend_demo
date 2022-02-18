from fastapi import APIRouter,Depends,status
from Model import schemas,models
from Security.jwt_bearer import JWTBearer
from DB.database import get_db ,SessionLocal
from uuid import uuid4
from sqlalchemy.orm import session
from Security.jwt_handler import signJWT
from Security.utils import verify

router = APIRouter()
db = SessionLocal()



  
@router.post('/serviceman/login',tags=['SERVICEMAN_ROLE'])
def serviceman_login(user_credentials:schemas.AZAUser_login,db:session=Depends(get_db)):

    user = db.query(models.AZAserviceman).filter(models.AZAserviceman.mobile_number==user_credentials.mobile_number).first()
    
    if not user:

   
     return{"error_message": "There was a problem with your login","status":status.HTTP_404_NOT_FOUND}
    
    if not verify(user_credentials.password,user.password):
       
        return{"error_message":  "There was a problem with your login","status":status.HTTP_404_NOT_FOUND}

    token = signJWT( user_credentials.mobile_number )
    
    fname = db.query(models.AZAserviceman.name).filter(models.AZAserviceman.mobile_number==user_credentials.mobile_number).first()
    fl_id =db.query(models.AZAserviceman.id).filter(models.AZAserviceman.mobile_number==user_credentials.mobile_number).first()
    

    return  {'user_data':{

                **fl_id,
                **fname,
                'mobile_number': int(user_credentials.mobile_number) ,
                "access_token" :token,  
                "token_type":"Bearer"
            },
     'status':status.HTTP_302_FOUND
    }


@router.get('/Serviceman_get_order',dependencies=[Depends(JWTBearer())],tags=['SERVICEMAN_ROLE'])
def get_an_order(user_id:int):

    package1 = db.query(models.Package).filter(models.Package.owner_id == user_id).all()
    package2 = db.query(models.Pickup_Address).filter(models.Pickup_Address.owner_id == user_id).all()
    package3 = db.query(models.Delivery_Address).filter(models.Delivery_Address.owner_id == user_id).all()
    package4 = db.query(models.Delivery_Details).filter(models.Delivery_Details.owner_id == user_id).all()
    return {'Package':package1 ,'Pickup_Address':package2,'Delivery_Address':package3,'Delivery_Details':package4}


