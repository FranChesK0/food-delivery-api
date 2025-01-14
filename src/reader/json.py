from typing import Any

import ujson

from schemas import (
    CategorySchema,
    RestaurantSchema,
    CategoryAddSchema,
    MenuItemAddSchema,
    ScheduleAddSchema,
    RestaurantAddSchema,
)


def load_restaurants(file_path: str) -> list[RestaurantAddSchema]:
    return [RestaurantAddSchema.model_validate(r) for r in _read_json_file(file_path)]


def load_schedules(
    file_path: str, restaurants: list[RestaurantSchema]
) -> list[ScheduleAddSchema]:
    return [
        ScheduleAddSchema.model_validate(
            {
                "restaurant_id": [r.id for r in restaurants if r.title == s["title"]][0],
                "start": s["start"],
                "end": s["end"],
            }
        )
        for s in _read_json_file(file_path)
    ]


def load_categories(file_path: str) -> list[CategoryAddSchema]:
    categories: list[CategoryAddSchema] = []
    data = _read_json_file(file_path)
    for restaurant in data:
        for category in restaurant["menu"]:
            category_name = category["category"]
            if category_name not in categories:
                categories.append(category_name)
    return [CategoryAddSchema.model_validate({"name": name}) for name in categories]


def load_menus(
    file_path: str, restaurants: list[RestaurantSchema], categories: list[CategorySchema]
) -> list[MenuItemAddSchema]:
    menus: list[MenuItemAddSchema] = []
    data = _read_json_file(file_path)
    for rest in data:
        restaurant_id = [r.id for r in restaurants if r.title == rest["restaurant"]][0]
        for category in rest["menu"]:
            category_id = [c.id for c in categories if c.name == category["category"]][0]
            for item in category["items"]:
                menus.append(
                    MenuItemAddSchema.model_validate(
                        {
                            "restaurant_id": restaurant_id,
                            "category_id": category_id,
                            "name": item["name"],
                            "price": item["price"],
                            "description": item["description"],
                        }
                    )
                )
    return menus


def _read_json_file(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as file:
        return ujson.load(file)
