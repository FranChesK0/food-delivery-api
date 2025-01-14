from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import ScheduleSchema, ScheduleAddSchema

from .models import Schedule


class ScheduleRepository:
    @classmethod
    @logger.catch
    async def add_one(
        cls, schedule: ScheduleAddSchema, session: AsyncSession
    ) -> ScheduleSchema:
        logger.debug(f"Adding {schedule}")
        schedule_dict = schedule.model_dump()
        schedule_orm = Schedule(**schedule_dict)
        session.add(schedule_orm)

        await session.flush()
        await session.commit()

        logger.info(f"Added {schedule}")
        return ScheduleSchema.model_validate(schedule_orm)

    @classmethod
    @logger.catch
    async def add_many(
        cls, schedules: list[ScheduleAddSchema], session: AsyncSession
    ) -> list[ScheduleSchema]:
        logger.debug(f"Adding {len(schedules)} schedules")
        schedule_dicts = [schedule.model_dump() for schedule in schedules]
        schedule_orms = [Schedule(**schedule_dict) for schedule_dict in schedule_dicts]
        session.add_all(schedule_orms)

        await session.flush()
        await session.commit()

        logger.info(f"Added {len(schedules)} schedules")
        return [
            ScheduleSchema.model_validate(schedule_orm) for schedule_orm in schedule_orms
        ]

    @classmethod
    @logger.catch
    async def find(cls, id: int, session: AsyncSession) -> ScheduleSchema:
        logger.debug(f"Finding schedule {id}")
        schedule_orm = await session.execute(select(Schedule).where(Schedule.id == id))
        schedule = schedule_orm.scalars().one_or_none()
        if schedule is None:
            raise ValueError(f"Schedule {id} not found")

        logger.info(f"Found schedule {id}")
        return ScheduleSchema.model_validate(schedule)

    @classmethod
    @logger.catch
    async def find_by_restaurant(
        cls, restaurant_id: int, session: AsyncSession
    ) -> ScheduleSchema:
        logger.debug(f"Finding schedule for {restaurant_id} restaurant")
        schedule_orm = await session.execute(
            select(Schedule).where(Schedule.restaurant_id == restaurant_id)
        )
        schedule = schedule_orm.scalars().one_or_none()
        if schedule is None:
            raise ValueError(f"Schedule for {restaurant_id} not found")

        logger.info(f"Found schedule for {restaurant_id} restaurant")
        return ScheduleSchema.model_validate(schedule)
