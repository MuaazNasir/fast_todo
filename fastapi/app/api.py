from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy.orm import Session
import json


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



app : FastAPI = FastAPI()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def convert_json(data):
    try:
        # Attempt to parse the data as JSON
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        # JSON decoding failed or the data is not a string
        return data
        
@app.post("/todos")
def add_todo(todo = Body(),db : Session = Depends(get_db)):
    todo_data = TodoCreate(**convert_json(todo))
    todo = Todo(**todo_data.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos/{id}")
def get_todo(id:int, db : Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo :
        return todo
    else :
        raise HTTPException(status_code=404,detail="todo not found")
    
@app.get("/todos")
def get_todo(db : Session = Depends(get_db)):
    todo = db.query(Todo).all()
    if todo :
        return todo
    else :
        raise HTTPException(status_code=404,detail="failed to fetch todos")

    
@app.put("/todos/{id}")
def update_todo(id:int, updated_todo = Body(), db : Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo:
        updated_data = convert_json(updated_todo)
        db.query(Todo).filter(Todo.id == todo.id)\
            .update(
                {Todo.title : updated_data["title"] or todo.title, Todo.description : updated_data["description"] or todo.description}
                )
        db.commit()
        db.refresh(todo)
        return todo
    else :
        raise HTTPException(status_code=404,detail="todo not found")
        

@app.delete("/todos/{id}")
def delete_todo(id : int, db : Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return {"deleted" : True}
    else:
        raise HTTPException(status_code=404,detail="todo not found")
