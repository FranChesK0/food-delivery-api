from fastapi import APIRouter

from schemas import RestaurantSchema
from repository import SessionDep, RestaurantRepository

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("", summary="Returns list of restaurants")
async def get_restaurants(session: SessionDep) -> list[RestaurantSchema]:
    return await RestaurantRepository.find_all(session)
