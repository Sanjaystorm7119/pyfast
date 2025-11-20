from fastapi import FastAPI 
# , Depends , HTTPException, Path , Query
# from pydantic import BaseModel, Field , ConfigDict
# from starlette import status
# from sqlalchemy.orm import Session
# from models import Dbmanager
from database import engine , SessionLocal 
import models
# from typing import Annotated
from router import auth, manager


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(manager.router)


