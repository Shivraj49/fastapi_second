import email
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings


#! VOLUNTEER AUTHENTICATION
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login_vol')

# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token_vol(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token_vol(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        v_email: str = payload.get("volunteer_email")
        if v_email is None:
            raise credentials_exception
        token_data = schemas.Token_data(v_email=v_email)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_volunteer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token_vol(token, credentials_exception) 

    volunteer = db.query(models.Volunteer_details).filter(models.Volunteer_details.v_email == token.v_email).first()

    return volunteer



#! COLLEGE AUTHENTICATION
oauth2_scheme_col = OAuth2PasswordBearer(tokenUrl='login_col')

SECRET_KEY = "34305tj4n4vimf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*182


def create_access_token_col(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token_col(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        c_code: int = payload.get("college_code")
        if c_code is None:
            raise credentials_exception
        token_data = schemas.Token_data_col(c_code=c_code)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_college(token: str = Depends(oauth2_scheme_col), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token_col(token, credentials_exception)

    college = db.query(models.Volunteer_details).filter(models.College_details.college_code == token.c_code).first()

    return college