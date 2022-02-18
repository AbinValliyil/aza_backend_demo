from fastapi import APIRouter,Depends,status
from Security.jwt_handler import signJWT
from Model import schemas,models
from Security.jwt_bearer import JWTBearer
from DB.database import get_db ,SessionLocal
from uuid import uuid4
from sqlalchemy.orm import session
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






@router.get('/Admin_get_allorder',dependencies=[Depends(JWTBearer())],tags=['ADMIN_ROLE'])
def get_an_order():

    package1 = db.query(models.Package).all()
    package2 = db.query(models.Pickup_Address).all()
    package3 = db.query(models.Delivery_Address).all()
    package4 = db.query(models.Delivery_Details).all()
   
   
    return {'Package':package1 ,'Pickup_Address':package2,'Delivery_Address':package3,'Delivery_Details':package4}


@router.get('/Admin_get_userorder',dependencies=[Depends(JWTBearer())],tags=['ADMIN_ROLE'])
def get_an_order(user_id:str):

    package1 = db.query(models.Package).filter(models.Package.owner_id == user_id).all()
    package2 = db.query(models.Pickup_Address).filter(models.Pickup_Address.owner_id == user_id).all()
    package3 = db.query(models.Delivery_Address).filter(models.Delivery_Address.owner_id == user_id).all()
    package4 = db.query(models.Delivery_Details).filter(models.Delivery_Details.owner_id == user_id).all()
    return {'Package':package1 ,'Pickup_Address':package2,'Delivery_Address':package3,'Delivery_Details':package4}




@router.post('/create_serviceman',dependencies=[Depends(JWTBearer())],tags=['ADMIN_ROLE'])

async def create_an_serviceman(user:schemas.AZA_SingUp,db:session=Depends(get_db)):
      
    db_user= db.query(models.AZAserviceman).filter(models.AZAserviceman.mobile_number ==user.mobile_number).first()

    if db_user is not  None:
        
        return{"error_message": "mobile number already exists!","status":status.HTTP_400_BAD_REQUEST}
          

    hashed_password = hash(user.password)
    user.password = hashed_password
      
    
    token =signJWT(user.mobile_number)

    new_user = models.AZAserviceman(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    f_id = db.query(models.AZAserviceman.id).filter(models.AZAserviceman.mobile_number==user.mobile_number).first()
    
    return {'serviceman_data':{

                  
              
             ** f_id,
             'name'           : user.name,
             'mobile_number'  :user.mobile_number,
             'access_token'   :token,
             'type':"Bearer"
                        
                        
            },
            'status':status.HTTP_201_CREATED
            } 
