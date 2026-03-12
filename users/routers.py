from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.users.models import Users
from app.users.schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["Работа с пользователями"])


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@router.get("/", summary="Получить всех пользователей", response_model=list[UserOut])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Users).order_by(Users.id))
    return list(result.scalars().all())


@router.get("/{user_id}", summary="Получить пользователя по id", response_model=UserOut)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


@router.post("/", summary="Создать пользователя", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    user = Users(**payload.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.delete(
    "/{user_id}",
    summary="Удалить пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    await session.execute(delete(Users).where(Users.id == user_id))
    await session.commit()
    return None
