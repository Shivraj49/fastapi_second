from fastapi import FastAPI, status, Depends,HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .. import models, utils, schemas
from .. database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import List

router= APIRouter(
    prefix="/admin",
    tags=["admin"]
)


#! CRETAE ADMIN
@router.post("/create", response_model=schemas.admin_out)
def create_volunteer(admin: schemas.college_in, db: Session = Depends(get_db),):

    
    new_admin = models.admin_(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin