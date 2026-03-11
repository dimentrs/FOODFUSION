from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class NewsletterSubscribeIn(BaseModel):
    email: EmailStr


class NewsletterSubscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime


class ContactMessageIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(min_length=1, max_length=5000)


class ContactMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    message: str
    created_at: datetime


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=220)
    description: str = Field(min_length=1)
    image_url: str | None = Field(default=None, max_length=500)


class RecipeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    slug: str
    description: str
    image_url: str | None
    created_at: datetime
    updated_at: datetime

