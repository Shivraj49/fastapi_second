from fastapi import FastAPI, status, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .. import models, utils, schemas
from .. database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/emergency",
    tags=["emergency"]
)

#! GET EMERGENCY CONTACTS BY AREA
@router.get("/city/{city}", response_model=schemas.emergency_out)
def get_emergency_details(city=str, db: Session = Depends(get_db),):

    emergency = db.query(models.Emergency_contact).filter(
        models.Emergency_contact.city == city).first()

    # if emergency does not exist
    if not emergency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Emergency contacts associated with city: {city} was not found")

    return emergency

#! GET EMERGENCY CONTACTS BY DISTRICT
@router.get("/district/{district}", response_model=List[schemas.emergency_out])
def get_emergency_details(district= str, db: Session = Depends(get_db),):

    emergency = db.query(models.Emergency_contact).filter(
        models.Emergency_contact.district == district).all()

    # if emergency does not exist
    if not emergency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Emergency contacts associated with District: {district} was not found")

    return emergency

