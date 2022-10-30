from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url="sqlite://tg_top.sqlite3",
        modules={"models": ["db.models"]}
    )
    await Tortoise.generate_schemas()


async def close_connection():
    await Tortoise.close_connections()
