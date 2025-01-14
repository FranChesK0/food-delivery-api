from fastapi import APIRouter

from schemas import CategorySchema, RestaurantSchema
from repository import (
    SessionDep,
    CategoryRepository,
    MenuItemRepository,
    RestaurantRepository,
)

router = APIRouter(prefix="/category", tags=["Categories"])


@router.get("", summary="Get all categories")
async def get_categories(session: SessionDep) -> list[CategorySchema]:
    return await CategoryRepository.find_all(session)


@router.get("/{category_id}/restaurants", summary="Get all restaurants in a category")
async def get_restaurants(
    category_id: int, session: SessionDep
) -> list[RestaurantSchema]:
    restaurants = {r.id: r for r in await RestaurantRepository.find_all(session)}
    items = await MenuItemRepository.find_by_category(category_id, session)

    result: list[RestaurantSchema] = []
    for item in items:
        if item.restaurant_id not in [i.id for i in result]:
            result.append(restaurants[item.restaurant_id])

    return result
