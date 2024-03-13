from sqlalchemy import insert, select
from sqlalchemy import and_, delete, insert, select
from src.sub.models import sub
from src.database import async_session_maker



class SubService:

    @classmethod
    async def check_subscribe(cls, user_id, sub_id):
        async with async_session_maker() as session:
            query = select(sub).where(and_(sub.c.user_id == user_id, sub.c.sub_id == sub_id))
            result = await session.execute(query)
            return result.mappings().first() is not None