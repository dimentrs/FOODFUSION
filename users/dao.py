from sqlalchemy import select
from app.users.models import Users
from app.database import async_session_maker


class UsersDAO:
    @classmethod
    async def find_all_students(cls):
        async with async_session_maker() as session:
            query = select(Users)
            students = await session.execute(query)
            return students.scalars().all()
