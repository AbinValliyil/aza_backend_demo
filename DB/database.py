from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config



DB_URL = 'DB'


engine =create_engine( config( DB_URL,

#engine=create_engine('postgresql://postgres:123@localhost/AZA',
    echo=True
) )

print("Database ****** connected")

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionLocal=sessionmaker(bind = engine)