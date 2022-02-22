from fastapi import APIRouter,status,Depends
from Security.Random_OTP import OTPgenerator
import requests
from Model import schemas,models
from sqlalchemy.orm import session
from DB.database import get_db
from decouple import config

router=APIRouter()


    
@router.post('/OTP_Genarator/singup',tags=['MOBILE_OTP'])
async def otp(mobile_num:str,db:session=Depends(get_db)):
    db_user= db.query(models.AZAUser).filter(models.AZAUser.mobile_number ==mobile_num).first()

    if db_user is not  None:
        # raise HTTPException(status_code=400,error_message="mobile number already exists!")
        #return JSONResponse(status_code=400,content="mobile number already exists!")
        return{"error_message": "mobile number already exists! please login","status":status.HTTP_400_BAD_REQUEST}
           
    url ="https://www.fast2sms.com/dev/bulkV2"
    otp = OTPgenerator()
    mobile_number =mobile_num
    payload = f"variables_values={otp} , Team AZA Shiping Services! &route=otp&numbers={mobile_number}"
    headers = {
    'authorization':"1IJ6RkwgEFBm4i5YZdPD2SQj3GKrNebCh8xyOMTXopuv0HsUqlFfAkThdebIwMBYx7OE9tri2DlsRU1v",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }  
    
    response = requests.request("POST", url, data=payload, headers=headers)
    if not response:
        return{"status":status.HTTP_503_SERVICE_UNAVAILABLE}
   
    new_otp =models.AZAOTP(mobile_number=mobile_num,otp=otp)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)

    return {"status":status.HTTP_202_ACCEPTED,"mob":mobile_number} 

  

@router.post('/OTP_Genarator/resetpassword',tags=['MOBILE_OTP'])
async def otp(mobile_num:str,db:session=Depends(get_db)):
    url ="https://www.fast2sms.com/dev/bulkV2"
    otp = OTPgenerator()
    mobile_number =mobile_num
    payload = f"variables_values={otp} , Team AZA Shiping Services! &route=otp&numbers={mobile_number}"
    headers = {
    'authorization':"1IJ6RkwgEFBm4i5YZdPD2SQj3GKrNebCh8xyOMTXopuv0HsUqlFfAkThdebIwMBYx7OE9tri2DlsRU1v",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }  
    
    response = requests.request("POST", url, data=payload, headers=headers)
    if not response:
        return{"status":status.HTTP_503_SERVICE_UNAVAILABLE}
   
    new_otp =models.AZAOTP(mobile_number=mobile_num,otp=otp)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)

    return {"status":status.HTTP_202_ACCEPTED,"mob":mobile_number} 
    

@router.post('/otp_verification',tags=['MOBILE_OTP'])
def otp_verification(mobile:str,otp:str,db:session=Depends(get_db)):
     
    
    valid_otps = db.query(models.AZAOTP.otp).filter(models.AZAOTP.mobile_number==mobile).all()
    

    if valid_otps:
        valid_otp =list(valid_otps).pop()
        if valid_otp[0] == otp:
            return {"message":"OTP Verification Successfull","status":status.HTTP_202_ACCEPTED}
             
    return {"message":"Invalid OTP","status":status.HTTP_404_NOT_FOUND}
    

