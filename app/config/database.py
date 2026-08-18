from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config.secretes import secretes


if not secretes.DB_URL:
    raise RuntimeError("DB_URL environment variable is not set")


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    secretes.DB_URL,
    pool_pre_ping=True,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    async with SessionLocal() as db:
        yield db