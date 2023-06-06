
from typing import List, Union,Optional
from fastapi import UploadFile,Form
from pydantic import BaseModel
from datetime import datetime
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"



class create_schedule(BaseModel):
    schedule_content : str
    schedule_date : int
    schedule_time : int
    stress_step : int
    
    class Config:
        orm_mode = True

class modify_schedule(create_schedule):
    schedule_id : int
    
    class Config:
        orm_mode = True
        
class delete_schedule(BaseModel):

    schedule_id : int
    
    class Config:
        orm_mode = True
