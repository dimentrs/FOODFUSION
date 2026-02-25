from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])


@router.get("/")
async def get_index():
    return FileResponse("./index.html")
