from fastapi import APIRouter
from sqlalchemy.future import select
from app.database import async_session_maker
from app.users.models import Users
from app.users.dao import UsersDAO
from app.users.schemas import SUsers

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])


@router.get("/", summary="Получить всех пользователей", response_model=list[SUsers])
async def get_all_students():
    return await UsersDAO.find_all_students()
