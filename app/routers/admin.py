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
