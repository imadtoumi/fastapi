from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DB_USER= os.getenv("DB_USER")
DB_PASS= os.getenv("DB_PASS")
#Admin%40123
# Giving the url of my DB "Dont hardcode user and password"
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@192.168.1.12:30100/fastapi'

# Engine is reposinble for connection to the the DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This creates new Session for each request when it's called
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Base class for all ORM models (used to define database tables)
Base = declarative_base()

# Calling the sessionLocal to create a session to be able to Read/Write to/from the db
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()