from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import DATABASE


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]