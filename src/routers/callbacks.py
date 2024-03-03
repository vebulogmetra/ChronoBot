import logging
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import (
    create_event,
    delete_event,
    get_all_events,
    get_all_users,
    get_user_events,
    get_user_today_events,
)
from database.models import Event, User
from kb import KeyboardType, get_keyboard, get_remove_keyboard
from mappers import tg_to_db_format
from res import strings as st
from schemas import EventForDB, EventFromAPI, EventFromTelegramUser
from utils import remind_user

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == "fetch_user_events")
async def fetch_user_events_handler(clbck: CallbackQuery, db_session: AsyncSession):
    try:
        events: list[Event] = await get_user_events(
            db_session=db_session, user_id=clbck.from_user.id
        )
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
        await clbck.answer(st.server_error)
        return
    if events:
        for event in events:
            await clbck.message.answer(
                st.event_show.format(
                    title=event.title,
                    description=event.description,
                    expired_at=event.expired_at,
                    notify_at=event.notify_at,
                    created_at=event.created_at,
                    owner_id=event.owner_id,
                ),
                reply_markup=get_remove_keyboard(cb_data=f"delete_event_{event.id}"),
            )
    else:
        await clbck.message.answer(st.empty_events)


@router.callback_query(F.data == "fetch_user_today_events")
async def fetch_user_today_events_handler(clbck: CallbackQuery, db_session: AsyncSession):
    try:
        events: list[Event] = await get_user_today_events(
            db_session=db_session, user_id=clbck.from_user.id
        )
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
        await clbck.answer(st.server_error)
        return
    if events:
        for event in events:
            await clbck.message.answer(
                st.event_show.format(
                    title=event.title,
                    description=event.description,
                    expired_at=event.expired_at,
                    notify_at=event.notify_at,
                    created_at=event.created_at,
                    owner_id=event.owner_id,
                ),
                reply_markup=get_remove_keyboard(cb_data=f"delete_event_{event.id}"),
            )
    else:
        await clbck.message.answer(st.empty_events)


@router.callback_query(F.data == "save_event")
async def save_event_to_db_handler(
    clbck: CallbackQuery,
    state: FSMContext,
    db_session: AsyncSession,
    scheduler: AsyncIOScheduler,
    bot: Bot,
):
    user_event_data = await state.get_data()
    event_data: EventForDB = tg_to_db_format(EventFromTelegramUser(**user_event_data))
    await create_event(db_session=db_session, event_data=event_data)
    notify_at_str = datetime.strftime(event_data.notify_at, "%Y-%m-%d %H:%M:%S")
    await clbck.message.answer(
        st.event_saved.format(notify_at_str=notify_at_str),
        reply_markup=get_keyboard(KeyboardType.MENU),
    )
    month = event_data.notify_at.month
    day = event_data.notify_at.day
    hour = event_data.notify_at.hour
    minute = event_data.notify_at.minute

    remind_message = st.remind_text.format(
        expire_time=user_event_data.get("expire_time"),
        event_title=event_data.title,
        event_description=event_data.description,
    )
    scheduler.add_job(
        func=remind_user,
        trigger="cron",
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        args=(event_data.owner_id, remind_message, bot),
    )

    await state.clear()


@router.callback_query(F.data.startswith("delete_event_"))
async def remove_event_from_db_handler(clbck: CallbackQuery, db_session: AsyncSession):
    event_id: int = int(clbck.data.split("_")[2])
    await delete_event(db_session=db_session, event_id=event_id)
    await clbck.message.answer(
        st.event_deleted,
        reply_markup=get_keyboard(KeyboardType.MENU),
    )


@router.callback_query(F.data == "uptime_info")
async def show_uptime_info_handler(clbck: CallbackQuery, started_at: str):
    await clbck.message.answer(
        st.bot_started_at.format(started_at=started_at),
        reply_markup=get_keyboard(KeyboardType.ADMIN_MENU),
    )


@router.callback_query(F.data == "show_cronjobs")
async def show_scheduled_jobs_handler(clbck: CallbackQuery, scheduler: AsyncIOScheduler):
    scheduled_jobs = scheduler.get_jobs()
    if scheduled_jobs:
        job_list = "\n".join([str(job) for job in scheduled_jobs])
        await clbck.message.answer(f"Запланированные задачи:\n{job_list}")
    else:
        await clbck.message.answer("Нет запланированных задач")


@router.callback_query(F.data == "fetch_all_users")
async def show_all_users_handler(clbck: CallbackQuery, db_session: AsyncSession):
    try:
        users: list[User] = await get_all_users(db_session=db_session)
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
        await clbck.answer(st.server_error)
        return
    if users:
        for idx, u in enumerate(users, start=1):
            await clbck.message.answer(
                f"user {idx}, id = {u.id}",
                reply_markup=get_keyboard(KeyboardType.ADMIN_MENU),
            )
    else:
        await clbck.message.answer(st.empty_events)


@router.callback_query(F.data == "fetch_all_events")
async def fetch_all_events_handler(clbck: CallbackQuery, db_session: AsyncSession):
    try:
        events: list[dict] = await get_all_events(db_session=db_session)
    except Exception as e:
        logger.error(f"Ошибка БД: {e}")
        await clbck.answer(st.server_error)
        return
    if events:
        for event in events:
            await clbck.message.answer(
                st.event_show.format(
                    title=event.title,
                    description=event.description,
                    expired_at=event.expired_at,
                    notify_at=event.notify_at,
                    created_at=event.created_at,
                    owner_id=event.owner_id,
                ),
                reply_markup=get_keyboard(KeyboardType.ADMIN_MENU),
            )
    else:
        await clbck.message.answer(st.empty_events)
