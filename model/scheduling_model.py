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

class Schedule(Base):
    __tablename__ = "scheduling"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, nullable=False)
    schedule_content = Column(String(255))
    schedule_date = Column(Integer)
    schedule_time = Column(Integer)
    stress_step = Column(Integer)
    created_time = Column(DateTime)
