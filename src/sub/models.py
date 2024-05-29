from datetime import datetime

from fastapi_users.db import BaseUserDatabase
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Table, func)

from src.database import Base, metadata

# Определение таблицы sub с помощью SQLAlchemy
sub = Table(
    "sub",  # Имя таблицы в базе данных
    metadata,  # Метаданные для таблицы
    Column("id", Integer, primary_key=True),  # Уникальный идентификатор подписки
    Column("user_id", Integer, nullable=False),  # Идентификатор пользователя
    Column("sub_id", Integer, nullable=False)  # Идентификатор подписки
)


# Определение класса Sub, который наследует Base
class Sub(Base):
    __tablename__ = "sub"  # Имя таблицы в базе данных
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор подписки
    user_id = Column(Integer, nullable=False)  # Идентификатор пользователя
    sub_id = Column(Integer, nullable=False)  # Идентификатор подписки

    class Config:
        from_attributes = True  # Настройка конфигурации, указывающая на использование атрибутов
