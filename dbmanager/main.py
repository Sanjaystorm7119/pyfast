from fastapi import FastAPI , Depends , HTTPException, Path , Query
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from models import Dbmanager
from database import engine , SessionLocal 
import models
from typing import Annotated

app = FastAPI()
models.Base.metadata.create_all(bind=engine)




def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

class Dbmanager_schema(BaseModel):
    fname : str = Field(min_length=2)
    lname : str = Field(min_length=2)
    mobile : int = Field(ge=5_000_000_000 ,lt=10_000_000_000 )

    
@app.get('/readall', status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Dbmanager).all()


@app.get('/dbmanager/{id}', status_code=status.HTTP_200_OK)
async def read_tsk(db:db_dependency, id : int = Path(gt=0, le=100)):
    read_task_model = db.query(Dbmanager).filter(Dbmanager.id == id).first()
    if read_task_model is not None:
        return read_task_model
    raise HTTPException(status_code=404 , detail="not found")

@app.post('/add_record', status_code=status.HTTP_201_CREATED)
async def add_record(db: db_dependency , record_req: Dbmanager_schema):
    record_model = Dbmanager(**record_req.model_dump())

    db.add(record_model)
    db.commit()

