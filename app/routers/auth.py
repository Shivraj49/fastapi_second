
from pyexpat import model
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
#from app import oauth2
from .. import schemas, models, utils ,oauth2
from .. database import get_db

router = APIRouter(tags=['Authentication'])



#! VOLUNTEER AUTHENTICATION
@router.post("/login_vol", response_model=schemas.Token)
def login_vol(volunteer_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    volunteer = db.query(models.Volunteer_details).filter(
        models.Volunteer_details.v_email == volunteer_credentials.username).first()

    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Email")

    if not utils.verify(volunteer_credentials.password, volunteer.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password")

    # create a token
    # return token
    access_token_vol = oauth2.create_access_token_vol(
        data={"volunteer_email": volunteer_credentials.username})

    return {"access_token_vol": access_token_vol, "token_type": "bearer"}


#! COLLEGE AUTHENTICATION
@router.post("/login_col", response_model=schemas.Token_col)
def login_col(college_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    volunteer = db.query(models.College_details).filter(
        models.College_details.college_code == college_credentials.username, models.College_details.password == college_credentials.password).first()

    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    # create a token
    # return token
    access_token_col = oauth2.create_access_token_col(
        data={"college_code": college_credentials.username})

    return {"access_token_col": str(access_token_col), "token_type": "bearer"}



#! ADMIN AUTHENTICATION
@router.post("/login_admin")
def login_admin(admin_credentials: schemas.admin_auth, db: Session = Depends(get_db)):

    admin_ = db.query(models.admin_).filter(
        models.admin_.UID == admin_credentials.uid , models.admin_.password == admin_credentials.password).first()

    if admin_ == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
        
    return {"Successful": "login"}

  
