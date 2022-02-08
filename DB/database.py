from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine( "postgresql://hlspjaposfiork:1c0945f2cbb6ec823a6337d8e37edf866236fc16e94eb835834ca74b64c248dc@ec2-3-227-55-25.compute-1.amazonaws.com:5432/dcvgca83nsk5js",

#engine=create_engine('postgresql://postgres:123@localhost/AZA',
    echo=True
)

print("Database ****** connected")

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionLocal=sessionmaker(bind = engine)