from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# mysql://<username>:<password>@<host>:<port>/<db_name>
# mysql://root:root@localhost:3306/library
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@db:3306/library"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()