from enum import unique
from multiprocessing import Value
from pickle import TRUE
from unicodedata import name
from sqlalchemy.dialects.postgresql import UUID
from .database import SQLALCHEMY_DATABASE_URL, Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy

class College_details(Base):
    __tablename__ = "college_details"
    
    UID = Column(String, nullable=False) 
    college_code = Column(Integer, nullable=False, primary_key= True ,unique=True)
    college_name = Column(String, nullable=False, unique=True)
    district = Column(String, nullable=False) 
    city= Column( String, nullable = False)
    password = Column (String, nullable =False)

class Volunteer_details(Base): 
    __tablename__= "volunteer_details"  
    
    college_code= Column(Integer, nullable=False)
    first_name= Column(String, nullable= False) 
    last_name = Column (String, nullable= False)  
    v_email = Column (String, nullable= False, unique=True, primary_key= True)
    college_name = Column(String, nullable= False) 
    gender = Column(String, nullable=False)  
    age = Column (String, nullable= False)  
    contact_number = Column (String, nullable= False)
    city = Column(String, nullable= False)
    district = Column( String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    password= Column( String, nullable= False)  
    rating = Column (Integer, nullable = True)
 
class Emergency_contact(Base):
    __tablename__="emergency_contact"
    
    city = Column(String, nullable= False, unique= True, primary_key= True)
    district= Column(String, nullable = False)
    ambulance = Column(Integer, nullable= False)
    police_station = Column(Integer, nullable = False)
    fire_brigade = Column(Integer, nullable= False)
    NDRF_helpline_number= Column(Integer, nullable= False)
      
    
class admin_District_details(Base):
    __tablename__ = "district_details"
    
    UID = Column (String, unique= True, nullable= False, primary_key= True)
    district= Column(String, nullable= False, unique= True)
     
class admin_(Base):
    __tablename__= "ndrf_admin"
     
    UID = Column (String, unique= True, nullable= False, primary_key= True)
    password = Column(String, nullable= False) 
    

    