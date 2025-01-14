from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import RestaurantSchema, RestaurantAddSchema

from .models import Restaurant


class RestaurantRepository:
    @classmethod
    @logger.catch
    async def add_one(
        cls, restaurant: RestaurantAddSchema, session: AsyncSession
    ) -> RestaurantSchema:
        logger.debug(f"Adding {restaurant}")
        restaurant_dict = restaurant.model_dump()
        restaurant_orm = Restaurant(**restaurant_dict)
        session.add(restaurant_orm)

        await session.flush()
        await session.commit()

        logger.info(f"Added {restaurant}")
        return RestaurantSchema.model_validate(restaurant_orm)

    @classmethod
    @logger.catch
    async def add_many(
        cls, restaurants: list[RestaurantAddSchema], session: AsyncSession
    ) -> list[RestaurantSchema]:
        logger.debug(f"Adding {len(restaurants)} restaurants")
        restaurant_dicts = [restaurant.model_dump() for restaurant in restaurants]
        restaurant_orms = [
            Restaurant(**restaurant_dict) for restaurant_dict in restaurant_dicts
        ]
        session.add_all(restaurant_orms)

        await session.flush()
        await session.commit()

        logger.info(f"Added {len(restaurants)} restaurants")
        return [
            RestaurantSchema.model_validate(restaurant_orm)
            for restaurant_orm in restaurant_orms
        ]

    @classmethod
    @logger.catch
    async def find_all(cls, session: AsyncSession) -> list[RestaurantSchema]:
        logger.debug("Finding all restaurants")
        restaurant_orms = await session.execute(select(Restaurant))
        restaurants = restaurant_orms.scalars().all()
        logger.info(f"Found {len(restaurants)} restaurants")
        return [RestaurantSchema.model_validate(restaurant) for restaurant in restaurants]
