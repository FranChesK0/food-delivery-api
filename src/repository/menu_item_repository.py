from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import MenuItemSchema, MenuItemAddSchema

from .models import MenuItem


class MenuItemRepository:
    @classmethod
    @logger.catch
    async def add_one(
        cls, menu_item: MenuItemAddSchema, session: AsyncSession
    ) -> MenuItemSchema:
        logger.debug(f"Adding {menu_item}")
        menu_item_dict = menu_item.model_dump()
        menu_item_orm = MenuItem(**menu_item_dict)
        session.add(menu_item_orm)

        await session.flush()
        await session.commit()

        logger.info(f"Added {menu_item}")
        return MenuItemSchema.model_validate(menu_item_orm)

    @classmethod
    @logger.catch
    async def add_many(
        cls, menu_items: list[MenuItemAddSchema], session: AsyncSession
    ) -> list[MenuItemSchema]:
        logger.debug(f"Adding {len(menu_items)} menu items")
        menu_item_dicts = [menu_item.model_dump() for menu_item in menu_items]
        menu_item_orms = [
            MenuItem(**menu_item_dict) for menu_item_dict in menu_item_dicts
        ]
        session.add_all(menu_item_orms)

        await session.flush()
        await session.commit()

        logger.info(f"Added {len(menu_items)} menu items")
        return [
            MenuItemSchema.model_validate(menu_item_orm)
            for menu_item_orm in menu_item_orms
        ]

    @classmethod
    @logger.catch
    async def find_by_restaurant(
        cls, restaurant_id: int, session: AsyncSession
    ) -> list[MenuItemSchema]:
        logger.debug(f"Finding menu items for {restaurant_id} restaurant")
        menu_item_orms = await session.execute(
            select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
        )
        menu_items = menu_item_orms.scalars().all()
        logger.info(f"Found {len(menu_items)} menu items for {restaurant_id} restaurant")
        return [MenuItemSchema.model_validate(menu_item) for menu_item in menu_items]

    @classmethod
    @logger.catch
    async def find_by_category(
        cls, category_id: int, session: AsyncSession
    ) -> list[MenuItemSchema]:
        logger.debug(f"Finding menu items for {category_id} category")
        menu_item_orms = await session.execute(
            select(MenuItem).where(MenuItem.category_id == category_id)
        )
        menu_items = menu_item_orms.scalars().all()
        logger.info(f"Found {len(menu_items)} menu items for {category_id} category")
        return [MenuItemSchema.model_validate(menu_item) for menu_item in menu_items]
