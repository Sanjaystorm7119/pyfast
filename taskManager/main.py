from fastapi import FastAPI , Depends , HTTPException , Path, Query
from sqlalchemy.orm import Session
from typing import Annotated
import models
from models import TaskManager
from database import engine , SessionLocal 

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.get('/readall')
async def read_all(db:db_dependency):
    return db.query(TaskManager).all()


@app.get('/taskmanager/{id}')
async def read_task(db:db_dependency,id : int = Path(gt=0)):
    read_task_model = db.query(TaskManager).filter(TaskManager.id == id).first()
    if read_task_model is not None:
        return read_task_model
    raise HTTPException(status_code=404 , detail="not found")


