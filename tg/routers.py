import os
from http.client import HTTPException
from fastapi import APIRouter, requests
import requests
from starlette.responses import FileResponse
from pydantic import EmailStr

from app.tg.models import TelegramResponse
from app.config import TELEGRAM_API_URL, settings

router = APIRouter(prefix='/send_message', tags=['Telegram_Bot'])


def send_to_telegram(chat_id: int, message: str) -> TelegramResponse:
    try:
        response = requests.post(
            TELEGRAM_API_URL,
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            },
            timeout=10
        )
        data = response.json()
        return TelegramResponse(ok=data.get("ok", False), description=data.get("description"))
    except Exception as e:
        return TelegramResponse(ok=False, description=str(e))


@router.post("/send-message")
async def send_message(
    name: str,
    email: EmailStr,
    message: str
):

    text = (
        f"📩 <b>Новое сообщение с сайта</b>\n\n"
        f"👤 Имя: {name}\n"
        f"✉️ Email: {email}\n"
        f"💬 Сообщение: \n{message}"
    )

    target_chat_id = int(settings.TELEGRAM_CHAT_ID)
    send_to_telegram(target_chat_id, text)
    result = send_to_telegram(target_chat_id, text)

    if not result.ok:
        raise HTTPException()

    return {"status": "success", "message": "Сообщение отправлено"}


