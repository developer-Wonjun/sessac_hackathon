
from typing import List, Union,Optional
from fastapi import UploadFile,Form
from pydantic import BaseModel
from datetime import datetime
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

class UuidCheck(BaseModel):

    uuid:str
    class Config:
        orm_mode = True

class SignUp(UuidCheck):
    nickname : Optional[str] = None
    character_type : Optional[int] = None
    class Config:
        orm_mode = True
