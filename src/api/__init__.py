from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import menu, order, places, category, restaurants


def setup_app(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(menu.router)
    app.include_router(order.router)
    app.include_router(places.router)
    app.include_router(category.router)
    app.include_router(restaurants.router)


__all__ = ["setup_app"]
