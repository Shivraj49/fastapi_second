#Schemas
from ast import Pass
from lib2to3.pytree import Base
from uuid import UUID
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import psycopg2
from sqlalchemy import Column,Integer,String,TIMESTAMP,Boolean,ForeignKey
from datetime import datetime, time

#Schemas
#!ADMIN
class admin_in(BaseModel):
    UID : str
    password : str
    
#!COLLEGE
# TODO REQUEST
class college_in(BaseModel):
    UID : str
    college_code : int 
    college_name : str
    district :str
    city :str
    password : str

# TODO RESPONSE
class college_out(BaseModel):
    college_code: int
    college_name: str
    district: str
    
    class Config:
        orm_mode = True
       
#! VOLUNTTER
# TODO REQUEST
class volunteer_in(BaseModel):
    college_code: int
    first_name: str
    last_name : str
    v_email :EmailStr
    college_name :str
    gender :str
    age :int
    contact_number:str 
    city :str
    district :str            
    password: str
    
class volunteer_out(BaseModel):
    college_code: int
    first_name: str
    last_name : str
    v_email :EmailStr
    college_name :str
    gender :str
    age :int
    contact_number:str 
    city :str
    district :str 
    
    class Config:
        orm_mode = True
    
#TODO UPDATE VOLUNTEER
class volunteer_update_in(BaseModel):
    v_email: EmailStr
    contact_number: str
    
class volunteer_update_out(volunteer_out):
    Pass
    
    class Config:
        orm_mode = True

#! EMERGENCY
#TODO EMERGENCY OUT
class emergency_out(BaseModel):
    ambulance : int
    police_station : int
    fire_brigade : int
    NDRF_helpline_number: int
    
    class Config:
        orm_mode = True
        
#! AUTHENTICATION
#TODO REQUEST
class volunteer_login(BaseModel):
    v_email: EmailStr
    password: str
    
#! TOKEN Volunteer
class Token(BaseModel):
    access_token_vol: str 
    token_type: str
    
class Token_data(BaseModel):
    v_email: EmailStr 
    
#! TOKEN COLLEGE

class Token_col(BaseModel):
    access_token_col: str
    token_type: str
    
class Token_data_col(BaseModel):
    c_code : int


#!ADMIN 
class admin_auth(BaseModel):
    uid : str
    password : str