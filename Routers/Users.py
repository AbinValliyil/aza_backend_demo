from operator import iadd
from token import EQUAL
from fastapi import APIRouter, Depends,status,HTTPException
from Model.models import AZAUser
from Model import schemas,models
from Security.jwt_handler import signJWT
from Security.utils import verify,hash
from Security.Random_OTP import OTPgenerator
from DB.database import Base, engine,get_db ,SessionLocal
from sqlalchemy.orm import session
from fastapi import Request, HTTPException
import requests


router=APIRouter()
db = SessionLocal()


@router.post('/create_user',tags=['SIGN_UP'])

async def create_an_user(user:schemas.AZA_SingUp,db:session=Depends(get_db)):
      
    db_user= db.query(AZAUser).filter(models.AZAUser.mobile_number ==user.mobile_number).first()

    if db_user is not  None:
        # raise HTTPException(status_code=400,error_message="mobile number already exists!")
        #return JSONResponse(status_code=400,content="mobile number already exists!")
        return{"error_message": "mobile number already exists!","status":status.HTTP_400_BAD_REQUEST}
          

    hashed_password = hash(user.password)
    user.password = hashed_password
      
    
    token =signJWT(user.mobile_number)

    new_user = models.AZAUser(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    f_id = db.query(models.AZAUser.id).filter(models.AZAUser.mobile_number==user.mobile_number).first()
    
    return {'user_data':{

                  
              
             ** f_id,
             'name'           : user.name,
             'mobile_number'  :user.mobile_number,
             'access_token'   :token,
             'type':"Bearer"
                        
                        
            },
            'status':status.HTTP_201_CREATED
            }    
    
@router.post('/login',tags=['SING_IN'])
def user_login(user_credentials:schemas.AZAUser_login,db:session=Depends(get_db)):

    user = db.query(models.AZAUser).filter(models.AZAUser.mobile_number==user_credentials.mobile_number).first()
    
    if not user:

    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect mobile_number or password!")
     #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There was a problem with your login")
    

       #return JSONResponse(status_code=400,content="Incorrect mobile or password!")
     return{"error_message": "There was a problem with your login","status":status.HTTP_404_NOT_FOUND}
    
    if not verify(user_credentials.password,user.password):
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There was a problem with your login")
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect mobile_number or password") 
        #return JSONResponse(status_code=400,content="Incorrect mobile or password!")
        return{"error_message":  "There was a problem with your login","status":status.HTTP_404_NOT_FOUND}

    token = signJWT( user_credentials.mobile_number )
    
    fname = db.query(models.AZAUser.name).filter(models.AZAUser.mobile_number==user_credentials.mobile_number).first()
    fl_id =db.query(models.AZAUser.id).filter(models.AZAUser.mobile_number==user_credentials.mobile_number).first()
    

    return  {'user_data':{

                **fl_id,
                **fname,
                'mobile_number': int(user_credentials.mobile_number) ,
                "access_token" :token,  
                "token_type":"Bearer"
            },
     'status':status.HTTP_302_FOUND
    }




@router.put('/Reset_password',tags=["User Reset password "])
async def reset(user:schemas.Resetpass,db:session=Depends(get_db)):
    
    users = db.query(models.AZAUser).filter(models.AZAUser.mobile_number==user.mobile_number).first()
    
    if not users:

    
     return{"error_message": "There was a problem with your password reset","status":status.HTTP_404_NOT_FOUND}
    
    hashed_password = hash(user.password)
    users.password  = hashed_password
    
    token = signJWT( user.mobile_number )
    
    fname = db.query(models.AZAUser.name).filter(models.AZAUser.mobile_number==user.mobile_number).first()
    fl_id =db.query(models.AZAUser.id).filter(models.AZAUser.mobile_number==user.mobile_number).first()
    

    db.add(users)
    db.commit()
    db.refresh(users)

    
    
    return  {'user_data':{

                **fl_id,
                **fname,
                'mobile_number': int(user.mobile_number) ,
                "access_token" :token,  
                "token_type":"Bearer"
            },
     'status':status.HTTP_302_FOUND }
    
  

