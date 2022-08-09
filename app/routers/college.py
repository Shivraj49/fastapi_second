
from fastapi import FastAPI, status, Depends,HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .. import models, utils, schemas
from .. database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import List

router= APIRouter(
    prefix="/college",
    tags=["colleges"]
)

#path Operations
@router.get("/")
def get_colllege_details(db: Session = Depends(get_db)):
    college = db.query(models.College_details).all()
    
    return college

#! GET COLLEGE BY COLLEGE CODE
@router.get("/{college_code}", response_model= schemas.college_out)
def get_college_details(college_code: int,db: Session = Depends(get_db),):
    
    college = db.query(models.College_details).filter(models.College_details.college_code == college_code).first()
    
    #if college does not exist
    if not college:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail= f"College with college_code: {college_code} not Found")
    
    return college

#! GET COLLEGE BY DISTRICT
@router.get("/district/{district}", response_model=List[schemas.college_out])

def get_colllege_details(district: str,db: Session = Depends(get_db)):
    college = db.query(models.College_details).filter(models.College_details.district == district).all()
    
    return college

#! GET COLLEGES USING UID
@router.get("/uid/{uid}", response_model= List[schemas.college_out])
def get_college_details(uid: str,db: Session = Depends(get_db),):
    
    college = db.query(models.College_details).filter(models.College_details.UID == uid).all()
    
    #if college does not exist
    if not college:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail= f"College with uid: {uid} was not Found")
    
    return college