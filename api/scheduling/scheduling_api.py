from sqlalchemy.orm import Session
from fastapi import  Depends,APIRouter
from datetime import datetime,date
from fastapi.responses import JSONResponse
from config.jwt_config import AuthHandler
from database.database import db
from model.account_model import User
from model.scheduling_model import Schedule
from schemas.scheduling_schemas import *

router = APIRouter()
auth_handler = AuthHandler()

stress = {
    0 : -10.75,
    1 : -8.6,
    2 : -6.45,
    3 : -4.3,
    4 : -2.15,
    5 : 0,
    6 : 1,
    7 : 2,
    8 : 3,
    9 : 4,
    10 : 5
}

@router.post('',
    description="""
<h1>일정 생성 API</h1>

---
<h2>요구 Body</h2>
- schedule_content : str - 일정 내용
- schedule_date : int - 일정 날짜  ex - 20230607
- schedule_time : int - 일정 시간 ex - 1830
- stress_step : int - 스트레스 지수 ex -  0 ~ 10 
             """,tags=["scheduling"])
def create_schedule(data :create_schedule ,uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        user = db.query(User).filter(User.uuid == uuid).one()
        user_point = user.point
        user_id = user.id
        schedule_content = data.schedule_content
        schedule_date = data.schedule_date
        schedule_time = data.schedule_time
        stress_step = data.stress_step
        now = datetime.now()
        
        create_schedule = Schedule(user_id = user_id,
                            schedule_content = schedule_content,
                            schedule_date = schedule_date,
                            schedule_time = schedule_time,
                            stress_step = stress_step,
                            created_time = now
                            
        )    
        db.add(create_schedule)
        
        # if user_point + stress[stress_step] < 0 :
        #     user.point = 0
        # else:
        user.point = user_point + stress[stress_step]
        
        db.commit()
        
        return JSONResponse({'msg': 'schedule created success'} ,status_code=201)
    
    except Exception as e:
        return JSONResponse({'error' : e}, status_code = 400)
    
@router.put('',
    description="""
<h1>일정 수정 API</h1>

---
내용 / 날짜 / 시간 / 지수 중 바뀌는 값이 단 1개여도, 모든 값 다 다시 보내주세요.<br><br>
예를들어<br>
if 시간만 바뀌는 경우 -> 기존 내용 / 기존 날짜 / 바뀐 시간 / 기존 지수<br>
이렇게 보내주시면 됩니다.
---
<h2>요구 Body</h2>
- schedule_id : int - 일정 ID
- schedule_content : str - 일정 내용
- schedule_date : int - 일정 날짜  ex - 20230607
- schedule_time : int - 일정 시간 ex - 1830
- stress_step : int - 스트레스 지수 ex -  0 ~ 10 
             """,tags=["scheduling"])
def modify_schedule(data :modify_schedule ,uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        schedule = db.query(Schedule).filter(Schedule.id == data.schedule_id).one()
        user = db.query(User).filter(User.uuid == uuid).one()
        user_point = user.point
        
        schedule_content = data.schedule_content
        schedule_date = data.schedule_date
        schedule_time = data.schedule_time
        stress_step = data.stress_step
        
        if schedule.stress_step != stress_step:
        #     if user_point - stress[schedule.stress_step] + stress[stress_step] < 0 :
        #         user.point = 0
        #     else:
            user.point = user_point - stress[schedule.stress_step] + stress[stress_step]

        schedule.schedule_content = schedule_content
        schedule.schedule_date = schedule_date
        schedule.schedule_time = schedule_time
        schedule.stress_step = stress_step
        
        db.commit()

        return JSONResponse({'msg': 'schedule modify success'} ,status_code=201)
    
    except Exception as e:
        return JSONResponse({'error' : e}, status_code = 400)


@router.delete('',
    description="""
<h1>일정 삭제 API</h1>

---
<h2>요구 Body</h2>
- schedule_id : int
             """,tags=["scheduling"])
def delete_schedule(data :delete_schedule ,uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        schedule = db.query(Schedule).filter(Schedule.id == data.schedule_id).one()
        user = db.query(User).filter(User.uuid == uuid).one()
        user_point = user.point
        stress_step = schedule.stress_step
        
        # if user_point - stress[stress_step] < 0:
        #     user.point = 0
        # else:
        user.point = user_point - stress[stress_step]
        
        db.query(Schedule).filter(Schedule.id == data.schedule_id).delete()
        
        db.commit()
            
        return JSONResponse({'msg': 'schedule delete success'} ,status_code=201)
    
    except Exception as e:
        return JSONResponse({'error' : e}, status_code = 400)
    
    
@router.get('/{schedule_date}',
    description="""
<h1>특정 날짜 일정 조회 API</h1>

---
<h2>요구 데이터</h2>
- {schedule_date} : int - 특정 날짜  ex  20230607
             """,tags=["scheduling"])
def get_all_schedule(schedule_date :int ,uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        user = db.query(User).filter(User.uuid == uuid).one()
        schedule = db.query(Schedule)\
            .filter(Schedule.schedule_date == schedule_date)\
            .filter(Schedule.user_id == user.id).all()
        
        return schedule
    
    except Exception as e:
        return JSONResponse({'error' : e}, status_code = 400)
    
@router.get('/detail/{schedule_id}',
    description="""
<h1>특정 일정 상세 조회 API</h1>

---
<h2>요구 데이터</h2>
- {schedule_id} : int - 일정 ID

전체조회 -> 특정 일정 상세조회의 프로세스 이니, 전체조회에서 수령한 ID를 넣어주시면 됩니다.
             """,tags=["scheduling"])
def get_detail_schedule(schedule_id :int ,uuid=Depends(auth_handler.auth_wrapper) ,db:Session=Depends(db)):
    
    try:
        user = db.query(User).filter(User.uuid == uuid).one()
        schedule = db.query(Schedule)\
            .filter(Schedule.id == schedule_id)\
            .filter(Schedule.user_id == user.id).one()
        
        return schedule
    
    except Exception as e:
        return JSONResponse({'error' : e}, status_code = 400)