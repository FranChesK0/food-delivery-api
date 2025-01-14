import asyncio

from repository import setup_database


def main() -> None:
    asyncio.run(setup_database())


if __name__ == "__main__":
    main()
