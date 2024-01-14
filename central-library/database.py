from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import time
import os
# mysql://<username>:<password>@<host>:<port>/<db_name>
# mysql://root:root@localhost:3306/library

def wait_for_db(db_uri):
    _local_engine = create_engine(db_uri)

    _LocalSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=_local_engine
    )

    up = False
    while not up:
        try:
            db_session = _LocalSessionLocal()
            db_session.execute(text("SELECT 1"))
            db_session.commit()
        except Exception as err:
            print(f"Connection error: {err}")
            up = False
        else:
            up = True

        time.sleep(2)


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:root@{os.getenv('DATABASE_HOST')}:3306/library"
wait_for_db(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()