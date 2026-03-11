from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(tags=["Pages"])


@router.get("/", include_in_schema=False)
async def get_index():
    return FileResponse("index.html")
