from fastapi import FastAPI , Depends , HTTPException, Path , Query, APIRouter
from pydantic import BaseModel, Field , ConfigDict
from starlette import status
from sqlalchemy.orm import Session
from models import Dbmanager
from database import SessionLocal 
from typing import Annotated



router = APIRouter  ()


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
    
    model_config = ConfigDict(
        orm_mode=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "fname": "Alice",
                "lname": "Smith",
                "mobile": 9123456789
            }
        }
        )

    
@router.get('/readall', status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Dbmanager).all()


@router.get('/dbmanager/{id}', status_code=status.HTTP_200_OK)
async def read_tsk(db:db_dependency, id : int = Path(gt=0, le=100)):
    read_task_model = db.query(Dbmanager).filter(Dbmanager.id == id).first()
    if read_task_model is not None:
        return read_task_model
    raise HTTPException(status_code=404 , detail="not found")

@router.post('/add_record', status_code=status.HTTP_201_CREATED)
async def add_record(db: db_dependency , record_req: Dbmanager_schema):
    record_model = Dbmanager(**record_req.model_dump())

    db.add(record_model)
    db.commit()

@router.put("/dbmanager/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def updateDBmanager(db: db_dependency, record_req: Dbmanager_schema, id: int=Path(gt=0) ):
    record_update = db.query(Dbmanager).filter(Dbmanager.id == id).first()
    if record_update is None :
        raise HTTPException(status_code=404 , detail="not found")

    record_update.fname = record_req.fname
    record_update.lname = record_req.lname    
    record_update.mobile = record_req.mobile    

    db.add(record_update)
    db.commit()

@router.delete("/dbmanager/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def updateDBmanager(db: db_dependency, id: int=Path(gt=0) ):
    record_delete = db.query(Dbmanager).filter(Dbmanager.id == id).first()
    if record_delete is None :  
        raise HTTPException(status_code=404 , detail="not found")
    db.delete(record_delete)
    db.commit()
