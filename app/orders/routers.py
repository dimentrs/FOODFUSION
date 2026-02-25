from fastapi import APIRouter
from sqlalchemy.future import select
from app.database import async_session_maker
from app.orders.models import Orders

router = APIRouter(prefix='/orders', tags=['Работа с заказами'])