from datetime import datetime

from fastapi_users.db import BaseUserDatabase
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Table, func)

from src.database import Base, metadata

message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String, nullable=False),
    Column("sender_id",Integer, ForeignKey("user.id")),
    Column("recipient_id", Integer, ForeignKey("user.id")),
    Column("timestamp", TIMESTAMP)
)


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable= False)
    sender_id = Column(Integer, ForeignKey("user.id"))
    recipient_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=func.now())
    class Config:
        from_attributes = True