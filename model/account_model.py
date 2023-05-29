# coding: utf-8
from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Date,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    text,
    DateTime,
    Boolean
)
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pytz import timezone

Base = declarative_base()
# metadata = Base.metadata

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    uuid = Column(String(100), nullable=False)
    nickname = Column(String(45))
    point = Column(Integer, nullable=False)
    character_type = Column(Integer, nullable=False)
    created_time = Column(DateTime)
    
