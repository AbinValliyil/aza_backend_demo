# from fastapi import APIRouter,status,Depends
# from Security.Random_OTP import OTPgenerator
# import requests
# from Model import schemas,models
# from sqlalchemy.orm import session
# from DB.database import get_db
# from decouple import config
# import razorpay

# router=APIRouter()


    
# @router.post('/payment',tags=['PAY'])
# async def pay(RS:int):
#     client = razorpay.Client(auth=("rzp_test_gy2OEpQuEEknY6", "oQUFyPYVObMGkHmgJu5o2P94"))
#     data = { "amount": RS, "currency": "INR", "receipt": "order_rcptid_11" }
#     payment = client.order.create(data=data)
#     return payment
    