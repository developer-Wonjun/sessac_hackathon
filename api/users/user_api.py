from sqlalchemy.orm import Session
from fastapi import  Depends,APIRouter
from datetime import datetime,date
from fastapi.responses import JSONResponse
from config.jwt_config import AuthHandler
from database.database import db
from model.account_model import User
from model.scheduling_model import Schedule
from model.user_model import *
from schemas.user_schemas import SignUp

router = APIRouter()
auth_handler = AuthHandler()


@router.get('/info',tags=["user"],
    description="""
<h1>유저 정보 가져오는 API</h1>

---
<h2>요구 헤더</h2>
- Authorization : token
             """ ,status_code=200)
def user_info(uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):

    try:
        user = db.query(User).filter(User.uuid == uuid).one()

        user_nickname = user.nickname
        user_character_type = user.character_type
        user_point = user.point
        user_created_time = str(user.created_time)

        return JSONResponse({'user_nickname' :  user_nickname,
                             'user_point' : user_point,
                             'user_created_time' : user_created_time}, status_code = 200)
    
    except Exception as e:
        return JSONResponse({'error ' : e}, status_code = 400)


@router.put('/info',
    description="""
<h1>닉네임 변경 API - 사용 안함</h1>

---
             """, tags=['user'], status_code = 201)
def change_info(data : SignUp,uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        change_nickname = data.nickname
        user = db.query(User).filter(User.uuid == uuid).one()

        user.nickname = change_nickname
        db.commit()
        
        return JSONResponse({'new_user_nickname' : change_nickname})
    
    except Exception as e:
        
        return JSONResponse({'error':e} , 400)
    
    
@router.delete('/secession',
    description="""
<h1>회원 탈퇴 API</h1>

---
<h2>요구 Body</h2>
- 없습니다. 헤더에 토큰만 넣어주세요. 
- API 완료 이후에는, 초기 로그인 화면으로 넘어가주세요.
             """, tags=['user'], status_code = 201)
def user_secession(uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        user = db.query(User).filter(User.uuid == uuid)
        user_id = user.one().id
        db.query(Schedule).filter(Schedule.user_id == user_id).delete()
        user.delete()
        
        db.commit()
        return JSONResponse({'msg' : 'all delete.'}, status_code = 200)
    
    except Exception as e:
        
        return JSONResponse({'error':e} , 400)
