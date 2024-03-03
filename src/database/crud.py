import logging
from datetime import datetime

from sqlalchemy import (and_, delete, func, select, update)
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (Event, User)
from schemas import (EventForDB, UserForDB)

logger = logging.getLogger(__name__)


async def create_event(db_session: AsyncSession, event_data: EventForDB):
    try:
        db_session.add(Event(**event_data.model_dump()))
        await db_session.commit()
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")


async def create_user(db_session: AsyncSession, user_data: UserForDB):
    try:
        db_session.add(User(**user_data.model_dump()))
        await db_session.commit()
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")


async def get_user_by_id(db_session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    try:
        result = await db_session.execute(stmt)
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
    if result:
        return result.scalars().first()
    else:
        return None


async def get_all_users(db_session: AsyncSession):
    stmt = select(User)
    try:
        result = await db_session.execute(stmt)
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
    if result:
        return result.scalars().all()
    else:
        return None


async def get_all_events(db_session: AsyncSession):
    stmt = select(Event)
    try:
        result = await db_session.execute(stmt)
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
    if result:
        return result.scalars().all()
    else:
        return None


async def get_user_events(db_session: AsyncSession, user_id: int):
    stmt = select(Event).where(
        and_(Event.owner_id == user_id, Event.is_happened == False)
    )
    try:
        result = await db_session.execute(stmt)
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
    if result:
        return result.scalars().all()
    else:
        return None


async def get_user_today_events(db_session: AsyncSession, user_id: int):
    stmt = select(Event).where(
        and_(
            Event.owner_id == user_id,
            func.DATE(Event.expired_at) == datetime.now().date(),
            Event.is_happened == False,
        )
    )
    try:
        result = await db_session.execute(stmt)
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
    if result:
        return result.scalars().all()
    else:
        return None


async def hide_event(db_session: AsyncSession, event_id: int):
    stmt = (
        update(Event)
        .where(Event.id == event_id)
        .values(
            is_happened=True,
        )
    )
    try:
        await db_session.execute(stmt)
        await db_session.commit()
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")


async def make_reminded_event(db_session: AsyncSession, event_id: int):
    stmt = (
        update(Event)
        .where(Event.id == event_id)
        .values(
            is_reminded=True,
            is_happened=True,
        )
    )
    try:
        await db_session.execute(stmt)
        await db_session.commit()
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")


async def delete_event(db_session: AsyncSession, event_id: int):
    stmt = delete(Event).where(Event.id == event_id)
    try:
        await db_session.execute(stmt)
        await db_session.commit()
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
