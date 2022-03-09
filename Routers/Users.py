from sqlalchemy import null
from fastapi import APIRouter, Depends,status,HTTPException,Response
from Model.models import AZAUser
from Model import schemas,models
from Security.jwt_handler import signJWT
from Security.utils import verify,hash
from Security.Random_OTP import OTPgenerator
from DB.database import Base, engine,get_db ,SessionLocal
from sqlalchemy.orm import session
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import requests
from Security.jwt_bearer import JWTBearer


router=APIRouter()
db = SessionLocal()


@router.post('/create_user',tags=['USER'])

async def create_an_user(user:schemas.AZA_SingUp, Authorize:dependencies=[Depends(JWTBearer())],db:session=Depends(get_db)):
      
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
    # content = {"status":200,**f_id, 'name' : user.name,'mobile_number':user.mobile_number }
    # response = JSONResponse(content=content)
    # response.set_cookie(key="Bearer",value=token,expires=2.592e+6,httponly=True,path ='/',samesite=None)
    # return response
    Authorize.set_access_cookies(token)
    return {'user_data':{

                  
              
             ** f_id,
             'name'           : user.name,
             'mobile_number'  :user.mobile_number,
#              'access_token'   :token,
#              'type':"Bearer"
                        
                        
            },
            'status':status.HTTP_201_CREATED
            }    
    
@router.post('/login',tags=['USER'])
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
    
    # content = {"status":200,**fl_id,**fname,'token':itoken, 'mobile_number': int(user_credentials.mobile_number)}
    # response = JSONResponse(content=content)
    # response.set_cookie(key="Bearer",value=token,expires=2.592e+6,path ='/',samesite=None,domain='azza.vercel.app')
    # return response
    
    # # response.set_cookie(key="access_token",value=f"Bearer {token}", httponly=True)  #set HttpOnly cookie in response
    # # return response


    return  {'user_data':{

                **fl_id,
                **fname,
                'mobile_number': int(user_credentials.mobile_number) ,
                "access_token" :token,  
                "token_type":"Bearer"
            },
     'status':status.HTTP_302_FOUND
    }




@router.put('/Reset_password',tags=["USER"])
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
    


@router.get("/cookie/",tags=['SET-COOKIE'])
def create_cookie(mobile_number:str,password = None):
    token1 = signJWT( mobile_number )
    content = {"message": "Come to the dark , we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="Bearer",value=token1,expires=60,samesite=None,secure=True,domain='azza.vercel.app')
    return response


@router.post("/cookie/",tags=['SET-COOKIE'])
def create_cookie(mobile_number:str,password = None):
    token1 = signJWT( mobile_number )
    content = {"message": "Come to the dark , we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="Bearer",value=token1,expires=60,httponly=True,samesite=None,secure=True,domain='azza.vercel.app')
    return response

# @router.post("/logout/",tags=['LOGOUT'])
# def drop_cookie():
    
#     content = {"message": "Clear cookies",
#                 "status":200}
#     response = JSONResponse(content=content)
#     response.set_cookie(key="Bearer",expires=0,httponly=False,path ='/',samesite=None)
#     return response

  
