from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.site.models import ContactMessage, NewsletterSubscription, Recipe
from app.site.schemas import (
    ContactMessageIn,
    NewsletterSubscribeIn,
    RecipeCreate,
    RecipeOut,
)

router = APIRouter(prefix="/api", tags=["Site API"])


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@router.post("/newsletter/subscribe")
async def newsletter_subscribe(
    payload: NewsletterSubscribeIn | None = None,
    email: str | None = Form(default=None),
    session: AsyncSession = Depends(get_session),
):
    resolved_email = (payload.email if payload is not None else email) if (payload or email) else None
    if not resolved_email:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="email is required")

    sub = NewsletterSubscription(email=str(resolved_email).lower().strip())
    session.add(sub)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        # already subscribed -> treat as success (idempotent)
    return {"status": "success"}


@router.post("/contact")
async def create_contact_message(
    payload: ContactMessageIn,
    session: AsyncSession = Depends(get_session),
):
    msg = ContactMessage(
        name=payload.name.strip(),
        email=str(payload.email).lower().strip(),
        message=payload.message.strip(),
    )
    session.add(msg)
    await session.commit()
    return {"status": "success"}


@router.get("/recipes", response_model=list[RecipeOut])
async def list_recipes(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Recipe).order_by(Recipe.id.desc()))
    return list(res.scalars().all())


@router.post("/recipes", response_model=RecipeOut)
async def create_recipe(payload: RecipeCreate, session: AsyncSession = Depends(get_session)):
    recipe = Recipe(
        title=payload.title.strip(),
        slug=payload.slug.strip().lower(),
        description=payload.description.strip(),
        image_url=payload.image_url.strip() if payload.image_url else None,
    )
    session.add(recipe)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="recipe slug must be unique") from e

    await session.refresh(recipe)
    return recipe

