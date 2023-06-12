from sqlalchemy.orm import Session
from fastapi import  Depends,APIRouter
from datetime import datetime,date
from fastapi.responses import JSONResponse
from config.jwt_config import AuthHandler
from database.database import db
from model.account_model import User
from schemas.account_schemas import SignUp, UuidCheck
router = APIRouter()
auth_handler = AuthHandler()


@router.post('/check',
    description="""
<h1>유저 존재 체크 API</h1>

---
<h2>요구 Body</h2>
- uuid : str<br>

<b>Response status code</b><br>
- 200 : 유저 존재 o -> 로그인 api 호출 <br>
- 201 : 유저 존재 x -> 회원가입 플로우 진입
             """,tags=["account"] ,status_code=201)
def user_check(data :UuidCheck ,db:Session=Depends(db)):
    uuid = data.uuid
    
    try:
        user = db.query(User).filter(User.uuid == uuid).one()

        return JSONResponse({'msg' : 'user exist'}, status_code = 200)
    
    except:
        return JSONResponse({'msg' : 'user not exist'}, status_code = 201)


@router.post('/signin',
    description="""
<h1>로그인 API</h1>

---
<h2>요구 Body</h2>
- uuid : str
             """,tags=["account"] ,status_code=201)
def login(data :UuidCheck ,db:Session=Depends(db)):
    uuid = data.uuid
    
    try:
        user = db.query(User).filter(User.uuid == uuid).one()
        token = auth_handler.encode_token(uuid)

        return JSONResponse({'token' :  token}, status_code = 201)
    
    except Exception as e:
        return JSONResponse({'msg' : e}, status_code = 412)
        

@router.post('/signup',
    description="""
<h1>회원가입 API</h1>

---
<h2>요구 Body</h2>
- uuid : str
- nickname : str
             """,tags=["account"] ,status_code=201)
def register(data :SignUp ,db:Session=Depends(db)):

    try:
        uuid = data.uuid
        if db.query(User).filter(User.uuid == uuid).first() != None:
            return JSONResponse({'msg': 'user exist'}, 412)
        nickname = data.nickname
        character_type = 1 # 디폴트 값
        point = 0 
        register_user = User(uuid = uuid,
                            nickname = nickname,
                            character_type = character_type,
                            point = point,
                            created_time = datetime.now()
        )    
        db.add(register_user)
        db.commit()
        token = auth_handler.encode_token(uuid)
        
        return JSONResponse({'token' : token}, status_code =201)
    except Exception as e:
        return JSONResponse({'msg': e}, 400)

# @router.get('/address',tags=["account"] ,status_code=200)
# def get_address(db:Session=Depends(db)):
    
#     address = db.query(Address).all()

#     return address

# @router.get('/job',tags=["account"] ,status_code=200)
# def get_job(db:Session=Depends(db)):
    
#     large_job = db.query(LargeJob).all()
    
#     return large_job
