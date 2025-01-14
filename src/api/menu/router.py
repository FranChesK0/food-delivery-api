from fastapi import APIRouter

from schemas import MenuItemSchema
from repository import SessionDep, CategoryRepository, MenuItemRepository

from .responses import Item, Menu

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/{restaurant_id}/composition", summary="Get menu composition")
async def get_menu(restaurant_id: int, session: SessionDep) -> Menu:
    menu_items: list[MenuItemSchema] = await MenuItemRepository.find_by_restaurant(
        restaurant_id, session
    )

    by_category: dict[int, list[MenuItemSchema]] = {}
    for item in menu_items:
        if item.category_id in by_category:
            by_category[item.category_id].append(item)
        else:
            by_category[item.category_id] = [item]

    items: list[Item] = []
    for category_id, category_items in by_category.items():
        category = await CategoryRepository.find(category_id, session)
        items.append(Item.model_validate({"category": category, "items": category_items}))

    return Menu.model_validate({"restaurant_id": restaurant_id, "items": items})
