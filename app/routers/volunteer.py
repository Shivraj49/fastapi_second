from enum import auto
from fastapi import FastAPI, status, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import psycopg2
from .. import models, oauth2, utils, schemas
from .. database import get_db
from sqlalchemy.orm import Session
from .. schemas import volunteer_in, college_in, volunteer_update_in, volunteer_update_out, college_out
from typing import List

router = APIRouter(
    prefix="/volunteer",
    tags=["volunteer"]
)

#! GET ALL VOLUNTEERS
@router.get("/", response_model=List[schemas.volunteer_out])
def get_volunteer_details(db: Session = Depends(get_db)):
    college = db.query(models.Volunteer_details).all()

    return college

#! GET VOLUNTTER BY EMAIL
@router.get("/{v_email}", response_model=schemas.volunteer_out)
def get_volunteer_details(v_email: str,db: Session = Depends(get_db)):
    college = db.query(models.Volunteer_details).filter(models.Volunteer_details.v_email == v_email).first()

    return college

#! GET VOLUNTEER BY COLLEGE CODE
@router.get("/college_code/{college_code}", response_model=List[schemas.volunteer_out])
def get_volunteer_details(college_code: int ,db: Session = Depends(get_db)):
    
    college = db.query(models.Volunteer_details).filter(models.Volunteer_details.college_code == college_code).all()
    
    if college == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"colunteer with college_code: {college_code} does not exist")
    return college

#! GET VOLUNTEER BY DISTRICT
@router.get("/district/{district}", response_model=List[schemas.volunteer_out])
def get_volunteer_details(district: str ,db: Session = Depends(get_db)):
    
    district = db.query(models.Volunteer_details).filter(models.Volunteer_details.district == district).all()
    
    if district == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Volunteer with District: {district} does not exist")
    return district

#! CRETAE VOLUNTTER
@router.post("/create")
def create_volunteer(volunteer: volunteer_in, db: Session = Depends(get_db),get_current_college: str = Depends(oauth2.get_current_college)):

    if get_current_college == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not Authorized")
        
    elif volunteer.college_code != get_current_college.college_code:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not Authorized")
    # Hashing Password
    hashed_pass = utils.hash(volunteer.password)
    volunteer.password = hashed_pass

    new_volunteer = models.Volunteer_details(**volunteer.dict())
    db.add(new_volunteer)
    db.commit()
    db.refresh(new_volunteer)

    return new_volunteer

#! UPDATE VOLLUNTEER
@router.put("/update/{v_email}", )
def update_volunteer(v_email: str, updated_volunteer: schemas.volunteer_update_in, db: Session = Depends(get_db), get_current_volunteer: str = Depends(oauth2.get_current_volunteer)):
    
    post_query = db.query(models.Volunteer_details).filter(
        models.Volunteer_details.v_email == v_email)
    
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with email: {v_email} does not exist")
    
    if get_current_volunteer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not Authorized")
        
    elif v_email != get_current_volunteer.v_email:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not Authorized")
                
    post_query.update(updated_volunteer.dict(), synchronize_session=False)

    db.commit()
    
    return status.HTTP_200_OK;
