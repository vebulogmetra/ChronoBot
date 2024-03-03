import logging
import re

from aiogram import Bot

logger = logging.getLogger(__name__)


def validate_time_string(time_str: str) -> bool:
    pattern = r"^(?:[0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
    if re.fullmatch(pattern, time_str):
        return True
    else:
        return False


async def remind_user(user_id: int, message: str, bot: Bot):
    logger.info(f"Напоминание отправлено: {user_id=}")
    await bot.send_message(user_id, message)
