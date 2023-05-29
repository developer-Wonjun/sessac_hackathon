from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.env import SQLALCHEMY_DATABASE_URL
# from config.env import SQLALCHEMY_DATABASE_URL_
#DB_URL은 "mysql+pymysql://[유저이름]:[비밀번호]@[호스트주소]:[포트번호]/[스키마이름]?charset=utf8"로 구성된다.

SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#엔진 생성

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#세션 생성

Base = declarative_base()

def db():
    db = Session()
    try:
        yield db
    except:
        db.close()
    finally:
        db.close()
#해당 클레스를 상속받아 db의 모델이나 orm클레스를 생성