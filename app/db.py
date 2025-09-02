from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/workouts")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
new_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()