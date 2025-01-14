from fastapi import APIRouter

from schemas import ScheduleSchema
from repository import SessionDep, ScheduleRepository

router = APIRouter(prefix="/places", tags=["Places"])


@router.get("/{restaurant_id}/schedule", summary="Returns schedule of a restaurant")
async def get_restaurant_schedule(
    restaurant_id: int, session: SessionDep
) -> ScheduleSchema:
    return await ScheduleRepository.find_by_restaurant(restaurant_id, session)
