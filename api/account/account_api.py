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


@router.post('/signin',tags=["account"] ,status_code=201)
def login(data :UuidCheck ,db:Session=Depends(db)):
    uuid = data.uuid
    
    try:
        user = db.query(User).filter(User.uuid == uuid).one()
        token = auth_handler.encode_token(uuid)

        return JSONResponse({'token' :  token}, status_code = 201)
    
    except:
        return JSONResponse({'msg' : 'user not exist'}, status_code = 412)
        

@router.post('/signup',tags=["account"] ,status_code=201)
def register(data :SignUp ,db:Session=Depends(db)):

    try:
        uuid = data.uuid
        nickname = data.nickname
        character_type = data.character_type
        
        register_user = User(uuid = uuid,
                            nickname = nickname,
                            character_type = character_type
        )    
        db.add(register_user)
        db.commit()
        token = auth_handler.encode_token(uuid)
        
        return JSONResponse({'token' : token}, status_code =201)
    except:
        return JSONResponse({'msg': 'err'}, 400)

# @router.get('/address',tags=["account"] ,status_code=200)
# def get_address(db:Session=Depends(db)):
    
#     address = db.query(Address).all()

#     return address

# @router.get('/job',tags=["account"] ,status_code=200)
# def get_job(db:Session=Depends(db)):
    
#     large_job = db.query(LargeJob).all()
    
#     return large_job