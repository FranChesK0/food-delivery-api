from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CategorySchema, CategoryAddSchema

from .models import Category


class CategoryRepository:
    @classmethod
    @logger.catch
    async def add_one(
        cls, category: CategoryAddSchema, session: AsyncSession
    ) -> CategorySchema:
        logger.debug(f"Adding {category}")
        category_dict = category.model_dump()
        category_orm = Category(**category_dict)
        session.add(category_orm)

        await session.flush()
        await session.commit()

        logger.info(f"Added {category}")
        return CategorySchema.model_validate(category_orm)

    @classmethod
    @logger.catch
    async def add_many(
        cls, categories: list[CategoryAddSchema], session: AsyncSession
    ) -> list[CategorySchema]:
        logger.debug(f"Adding {len(categories)} categories")
        category_dicts = [category.model_dump() for category in categories]
        category_orms = [Category(**category_dict) for category_dict in category_dicts]
        session.add_all(category_orms)

        await session.flush()
        await session.commit()

        logger.info(f"Added {len(categories)} categories")
        return [
            CategorySchema.model_validate(category_orm) for category_orm in category_orms
        ]

    @classmethod
    @logger.catch
    async def find(cls, id: int, session: AsyncSession) -> CategorySchema:
        logger.debug(f"Finding category {id}")
        category_orm = await session.execute(select(Category).where(Category.id == id))
        category = category_orm.scalars().one_or_none()
        if category is None:
            raise ValueError(f"Category {id} not found")

        logger.info(f"Found category {id}")
        return CategorySchema.model_validate(category)

    @classmethod
    @logger.catch
    async def find_all(cls, session: AsyncSession) -> list[CategorySchema]:
        logger.debug("Finding all categories")
        category_orms = await session.execute(select(Category))
        categories = category_orms.scalars().all()
        logger.info(f"Found {len(categories)} categories")
        return [CategorySchema.model_validate(category) for category in categories]
