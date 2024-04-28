from aiogram import Bot, Dispatcher
import os
import asyncio
from loguru import logger
from routers.messages import main_router
from tortoise import Tortoise
from alarm import alarms


async def start():
    bot = Bot(token=os.getenv("TG_TOKEN"))
    dp = Dispatcher()
    await Tortoise.init(
        db_url='sqlite://zovbot.db?cache=shared&timeout=5000',
        modules={'models': ['db.models']}
    )

    dp.include_router(main_router)

    try:
        logger.debug(f"Бот под именем {await bot.get_my_name()} появился онлайн")
        await asyncio.gather(
            dp.start_polling(bot),
            alarms(bot)
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())