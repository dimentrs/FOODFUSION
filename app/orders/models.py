from datetime import date
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    description: Mapped[str]
    date: Mapped[int]
    cost: Mapped[int]
    status: Mapped[str]

