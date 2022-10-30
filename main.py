from aiogram import Dispatcher

from db import init_db, close_connection


async def on_startup(dp: Dispatcher):
    await init_db()


async def on_shutdown(dp: Dispatcher):
    await close_connection()
