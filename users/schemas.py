from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    # В текущей схеме БД email хранится как int (см. Alembic).
    # Сохраняем этот тип, чтобы не ломать существующие миграции.
    email: int
    order_id: int


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

