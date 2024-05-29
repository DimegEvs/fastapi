from datetime import datetime
from fastapi_users.db import BaseUserDatabase
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Table)

from src.database import Base, metadata

# Определение таблицы user с помощью SQLAlchemy
user = Table(
    "user",  # Имя таблицы в базе данных
    metadata,  # Метаданные для таблицы
    Column("id", Integer, primary_key=True),  # Уникальный идентификатор пользователя
    Column("email", String, nullable=False),  # Адрес электронной почты пользователя
    Column("name", String, nullable=False),  # Имя пользователя
    Column("surname", String, nullable=False),  # Фамилия пользователя
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),  # Дата и время регистрации пользователя
    Column("hashed_password", String, nullable=False),  # Захешированный пароль пользователя
    Column("is_active", Boolean, default=True, nullable=False),  # Флаг активности пользователя
    Column("is_superuser", Boolean, default=False, nullable=False),  # Флаг суперпользователя
    Column("is_verified", Boolean, default=False, nullable=False),  # Флаг верифицированного пользователя
)


# Определение класса User, который наследует SQLAlchemyBaseUserTable и Base
class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор пользователя
    email = Column(String, nullable=False)  # Адрес электронной почты пользователя
    name = Column(String, nullable=False)  # Имя пользователя
    surname = Column(String, nullable=False)  # Фамилия пользователя
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)  # Дата и время регистрации пользователя
    hashed_password: str = Column(String(length=1024), nullable=False)  # Захешированный пароль пользователя
    is_active: bool = Column(Boolean, default=True, nullable=False)  # Флаг активности пользователя
    is_superuser: bool = Column(Boolean, default=False, nullable=False)  # Флаг суперпользователя
    is_verified: bool = Column(Boolean, default=False, nullable=False)  # Флаг верифицированного пользователя

    class Config:
        from_attributes = True  # Настройка конфигурации, указывающая на использование атрибутов
