from datetime import date
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from pydantic import BaseModel, EmailStr, ConfigDict

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[int] = mapped_column()
    order_id: Mapped[int]
