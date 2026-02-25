from pydantic import BaseModel


class TelegramResponse(BaseModel):
    ok: bool
    description: str | None = None
