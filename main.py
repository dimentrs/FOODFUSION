import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.tg.routers import router as tg_router
from app.users.routers import router as users_router
from app.orders.routers import router as orders_router
from app.pages import router as pages_router
from app.site.routers import router as site_router
load_dotenv()

app = FastAPI()

app.include_router(tg_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(pages_router)
app.include_router(site_router)

# Serve frontend assets when running the backend.
app.mount("/CSS", StaticFiles(directory="CSS"), name="css")
app.mount("/JS", StaticFiles(directory="JS"), name="js")
app.mount("/SCSS", StaticFiles(directory="SCSS"), name="scss")

# Разрешаем запросы со всех доменов (чтобы форма с фронтенда могла достучаться)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
