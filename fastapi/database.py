from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine : Engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    description = Column(String, index=True)
    
    
class TodoCreate(BaseModel):
    title: str
    description: str
    
def create_tables():
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__": 
    create_tables()