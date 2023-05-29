from sqlalchemy.orm import Session
from fastapi import  Depends,APIRouter
from datetime import datetime,date
from fastapi.responses import JSONResponse
from config.jwt_config import AuthHandler
from database.database import db
from model.account_model import User
from model.user_model import *
from schemas.user_schemas import SignUp

router = APIRouter()
auth_handler = AuthHandler()


@router.get('/info',tags=["user"] ,status_code=200)
def user_info(uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):

    try:
        user = db.query(User).filter(User.uuid == uuid).one()

        user_nickname = user.nickname
        user_character_type = user.character_type
        user_point = user.point
        user_created_time = str(user.created_time)

        return JSONResponse({'user_nickname' :  user_nickname,
                             'user_character_type' : user_character_type,
                             'user_point' : user_point,
                             'user_created_time' : user_created_time}, status_code = 200)
    
    except Exception as e:
        return JSONResponse({'error ' : e}, status_code = 400)


@router.put('/info', tags=['user'], status_code = 201)
def change_info(data : SignUp,uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        change_nickname = data.nickname
        user = db.query(User).filter(User.uuid == uuid).one()

        user.nickname = change_nickname
        db.commit()
        
        return JSONResponse({'new_user_nickname' : change_nickname})
    
    except Exception as e:
        
        return JSONResponse({'error':e} , 400)
    
    