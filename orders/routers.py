from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.orders.models import Orders
from app.orders.schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["Работа с заказами"])


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@router.get("/", summary="Получить все заказы", response_model=list[OrderOut])
async def get_all_orders(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Orders).order_by(Orders.id))
    return list(result.scalars().all())


@router.get("/{order_id}", summary="Получить заказ по id", response_model=OrderOut)
async def get_order(order_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Orders).where(Orders.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    return order


@router.post("/", summary="Создать заказ", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, session: AsyncSession = Depends(get_session)):
    order = Orders(**payload.model_dump())
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.delete(
    "/{order_id}",
    summary="Удалить заказ",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(order_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Orders).where(Orders.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")

    await session.execute(delete(Orders).where(Orders.id == order_id))
    await session.commit()
    return None