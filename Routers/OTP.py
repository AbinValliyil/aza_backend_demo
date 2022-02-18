from fastapi import APIRouter,status,Depends
from Security.Random_OTP import OTPgenerator
import requests
from Model import schemas,models
from sqlalchemy.orm import session
from DB.database import get_db
from decouple import config

router=APIRouter()



@router.post('/OTP_Genarator',tags=['MOBILE_OTP'])
async def otp(mobile_num:str,Opt:schemas.OTP,db:session=Depends(get_db)):

    URL =config('OTP_URL')
    otp = OTPgenerator()
    mobile_number =mobile_num
    payload = f"variables_values={otp} , Team AZA Shiping Services! &route=otp&numbers={mobile_number}"
    headers = {
    'authorization': config('OTP_AUTH'),
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }  
    
    response = requests.request("POST", URL, data=payload, headers=headers)
    
    new_otp =models.AZAOTP(**Opt.dict(),mobile_number=mobile_num,otp=otp)
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)

    return {"status":status.HTTP_202_ACCEPTED} 
    


@router.post('/otp_verification',tags=['MOBILE_OTP'])
def otp_verification(mobile:str,otp:str,Opt:schemas.OTP,db:session=Depends(get_db)):
     
    
    valid_otps = db.query(models.AZAOTP.otp).filter(models.AZAOTP.mobile_number==mobile).all()
    

    if valid_otps:
        valid_otp =list(valid_otps).pop()
        if valid_otp[0] == otp:
            return {"message":"OTP Verification Successfull","status":status.HTTP_202_ACCEPTED}
    
    return {"message":"Invalid OTP","status":status.HTTP_404_NOT_FOUND}
    
