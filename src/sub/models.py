from datetime import datetime

from fastapi_users.db import BaseUserDatabase
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Table, func)

from src.database import Base, metadata

sub = Table(
    "sub",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable= False),
    Column("sub_id", Integer, nullable=False)
)


class Sub(Base):
    __tablename__ = "sub"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    sub_id = Column(Integer, nullable=False)
    
    class Config:
        from_attributes = True