from  fastapi  import FastAPI,Depends
from DB.database import Base, engine
from Model import models
from Routers import Users,Zipcode
from fastapi.middleware.cors import CORSMiddleware
from  Security.jwt_bearer import JWTBearer

models.Base.metadata.create_all(bind=engine)# automatic Database table create  

app=FastAPI( title="AZA [Shiping Service]" ,

  contact={
        "name": "Abin_michael",

        "email": "abinvalliyil@gmail.com"
             
                          })
app.include_router(Users.router)
app.include_router(Zipcode.router)

origins = [
    "http://localhost:3000",
    "https://azza.vercel.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/token',dependencies=[Depends(JWTBearer())],tags=['Token Test'])
def Test():
    return "Token access  are you  happy "


@app.get('/',tags=['Server Test'])
def Test():
    return "Server Test"


