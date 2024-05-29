from sqlalchemy import insert, select
from sqlalchemy import and_, delete, insert, select
from src.sub.models import sub
from src.database import async_session_maker

# Определение класса сервиса для работы с подписками
class SubService:

    @classmethod
    async def check_subscribe(cls, user_id, sub_id):
        # Асинхронный метод для проверки подписки пользователя
        async with async_session_maker() as session:
            # Формирование запроса для проверки наличия подписки
            query = select(sub).where(and_(sub.c.user_id == user_id, sub.c.sub_id == sub_id))
            # Выполнение запроса
            result = await session.execute(query)
            # Возвращение результата проверки подписки (True, если подписка существует, иначе False)
            return result.mappings().first() is not None
