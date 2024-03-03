import asyncio
import logging
from datetime import datetime

from aiogram import (Bot, Dispatcher)
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.engine import (create_db, session)
from middlewares.db import DataBaseSession
from middlewares.schedule import SchedulerMiddleware
from routers.callbacks import router as callbacks_router
from routers.commands import router as commands_router
from routers.events import router as events_router
from settings import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


dp.include_router(commands_router)
dp.include_router(events_router)
dp.include_router(callbacks_router)


async def on_startup(bot):
    await create_db()
    scheduler.start()


async def on_shutdown(bot):
    scheduler.shutdown()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # пропуск обновлений
    await bot.delete_webhook(drop_pending_updates=True)
    # мидлварь для прокидывания планировщика
    dp.update.middleware(SchedulerMiddleware(scheduler=scheduler))
    # мидлварь для прокидывания ДБ сессии
    dp.update.middleware(DataBaseSession(session_pool=session))

    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(filename="logs/app.log", level=logging.INFO)
    asyncio.run(main())
