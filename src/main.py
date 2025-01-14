import asyncio

import uvicorn
from fastapi import FastAPI

from api import setup_app
from core import settings
from repository import setup_database

app = FastAPI()


def main() -> None:
    asyncio.run(setup_database())
    setup_app(app)
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
