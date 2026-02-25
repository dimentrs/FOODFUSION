import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.tg.routers import router as tg_router
from app.users.routers import router as users_router
from app.orders.routers import router as orders_router
from app.pages import router as pages_router
load_dotenv()

app = FastAPI()

app.include_router(tg_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(pages_router)

# Разрешаем запросы со всех доменов (чтобы форма с фронтенда могла достучаться)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
