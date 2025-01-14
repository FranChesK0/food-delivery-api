from typing import Annotated
from datetime import datetime
from collections.abc import AsyncGenerator

from loguru import logger
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Mapped, DeclarativeBase, declared_attr, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core import settings

engine = create_async_engine(settings.DATABASE_URL)
session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


class Model(AsyncAttrs, DeclarativeBase):
    """Abstract base class for all models."""

    __abstract__ = True
    _repr_columns_number: int = 1
    _repr_columns: tuple[str, ...] = tuple()

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, index=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __repr__(self) -> str:
        columns: list[str] = []
        for ind, column in enumerate(self.__table__.columns.keys()):
            if column in self._repr_columns or ind < self._repr_columns_number:
                columns.append(f"{column}={getattr(self, column)}")
        return f"<{self.__class__.__name__} [{', '.join(columns)}]>"

    def __str__(self) -> str:
        return self.__repr__()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session.

    Yields:
        AsyncSession: Database session
    """
    async with session_maker() as session:
        logger.debug("Session created")
        yield session
    logger.info("Session closed")


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def create_tables() -> None:
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    logger.info("Database tables created")


async def drop_tables() -> None:
    """Drop database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    logger.warning("Database tables dropped")
