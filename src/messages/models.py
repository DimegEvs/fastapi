from datetime import datetime

from fastapi_users.db import BaseUserDatabase
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Table, func)

from src.database import Base, metadata

# Определение таблицы message с помощью SQLAlchemy
message = Table(
    "message",  # Имя таблицы в базе данных
    metadata,  # Метаданные для таблицы
    Column("id", Integer, primary_key=True),  # Уникальный идентификатор сообщения
    Column("message", String, nullable=False),  # Текст сообщения
    Column("sender_id", Integer, ForeignKey("user.id")),  # Идентификатор отправителя сообщения, ссылающийся на таблицу user
    Column("recipient_id", Integer, ForeignKey("user.id")),  # Идентификатор получателя сообщения, ссылающийся на таблицу user
    Column("timestamp", TIMESTAMP),  # Время отправки сообщения
    Column("is_read", Boolean, default=False)  # Флаг, указывающий, прочитано ли сообщение
)

# Определение класса Message, который наследует Base
class Message(Base):
    __tablename__ = "message"  # Имя таблицы в базе данных
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор сообщения
    message = Column(String, nullable=False)  # Текст сообщения
    sender_id = Column(Integer, ForeignKey("user.id"))  # Идентификатор отправителя сообщения, ссылающийся на таблицу user
    recipient_id = Column(Integer, ForeignKey("user.id"))  # Идентификатор получателя сообщения, ссылающийся на таблицу user
    timestamp = Column(DateTime, default=func.now())  # Время отправки сообщения, по умолчанию текущее время
    is_read = Column(Boolean, default=False)  # Флаг, указывающий, прочитано ли сообщение

    class Config:
        from_attributes = True  # Настройка конфигурации, указывающая на использование атрибутов
