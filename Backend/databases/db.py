from dotenv import load_dotenv
load_dotenv()
from Backend.config import DATABASE_URL
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(DATABASE_URL,echo = True,pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind = engine, 
    autoflush=False,
    autocommit=False
    )
Base = declarative_base()


def get_db() :
    db =SessionLocal()
    return db
    

if __name__ == "__main__":
    print("database Initialized successfully")