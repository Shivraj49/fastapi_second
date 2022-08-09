from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
from . import models
from . database import engine, get_db
from sqlalchemy.orm import Session
from .routers import volunteer, college,auth, admin, emergency
from .config import settings

    
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(volunteer.router)
app.include_router(college.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(emergency.router)










