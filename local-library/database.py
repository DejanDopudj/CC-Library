from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import os
# mysql://<username>:<password>@<host>:<port>/<db_name>
# mysql://root:root@localhost:3306/library

time.sleep(30)
#env dodaj
print("Aaaaa")
print(os.getenv('DATABASE_PORT'))
try:
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:root@{os.getenv('DATABASE_HOST')}:3306/{os.getenv('LOCAL_DATABASE')}"
    print(SQLALCHEMY_DATABASE_URL)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
except:
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:root@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('LOCAL_DATABASE')}"
    print(SQLALCHEMY_DATABASE_URL)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()