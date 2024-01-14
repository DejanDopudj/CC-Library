from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import os
# mysql://<username>:<password>@<host>:<port>/<db_name>
# mysql://root:root@localhost:3306/library

time.sleep(30)
#env dodaj
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:root@{os.getenv('DATABASE_HOST')}:3306/library"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()