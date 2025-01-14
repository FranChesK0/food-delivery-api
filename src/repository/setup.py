import os

from loguru import logger

from core import settings
from reader import load_menus, load_schedules, load_categories, load_restaurants

from .database import drop_tables, create_tables, session_maker
from .category_repository import CategoryRepository
from .schedule_repository import ScheduleRepository
from .menu_item_repository import MenuItemRepository
from .restaurat_repository import RestaurantRepository

DATA_DIR: str = os.path.join(settings.BASE_DIR, "data", "preload")


async def setup_database() -> None:
    await drop_tables()
    await create_tables()

    async with session_maker() as session:
        restaurants = await RestaurantRepository.add_many(
            load_restaurants(os.path.join(DATA_DIR, "restaurants.json")), session
        )
        await ScheduleRepository.add_many(
            load_schedules(os.path.join(DATA_DIR, "schedules.json"), restaurants), session
        )
        categories = await CategoryRepository.add_many(
            load_categories(os.path.join(DATA_DIR, "menus.json")), session
        )
        await MenuItemRepository.add_many(
            load_menus(os.path.join(DATA_DIR, "menus.json"), restaurants, categories),
            session,
        )

    logger.info("Database preloaded")
