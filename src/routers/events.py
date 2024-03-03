from datetime import datetime as dt
from datetime import time

from aiogram import (F, Router)
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message)
from aiogram_calendar import (SimpleCalendar, SimpleCalendarCallback)

from kb import (KeyboardType, get_keyboard)
from mappers import tg_to_db_format
from res import strings as st
from schemas import (EventForDB, EventFromTelegramUser)
from states import CreateEvent
from utils import validate_time_string

router = Router()


@router.callback_query(F.data == "create_event")
async def create_event_handler(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(
        "Введите название события: ", reply_markup=get_keyboard(KeyboardType.EXIT)
    )
    await state.set_state(CreateEvent.enter_title)


@router.message(CreateEvent.enter_title, F.text)
async def title_entered(msg: Message, state: FSMContext):
    await state.update_data(owner_id=msg.from_user.id)
    await state.update_data(title=msg.text)
    await msg.answer(
        "Введите описание события: ", reply_markup=get_keyboard(KeyboardType.EXIT)
    )
    await state.set_state(CreateEvent.enter_description)


@router.message(CreateEvent.enter_description, F.text)
async def description_entered(msg: Message, state: FSMContext):
    reply_markup = await SimpleCalendar().start_calendar()
    await state.update_data(description=msg.text)
    await msg.answer("Выберите дату события: ", reply_markup=reply_markup)
    await state.set_state(CreateEvent.enter_expires_date)


@router.callback_query(CreateEvent.enter_expires_date, SimpleCalendarCallback.filter())
async def process_simple_calendar(
    clbck: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    calendar = SimpleCalendar()
    calendar.set_dates_range(dt(2022, 1, 1), dt(2025, 12, 31))
    selected, date = await calendar.process_selection(clbck, callback_data)
    if selected:
        await state.update_data(expire_date=date)
    else:
        await clbck.answer("Ошибка выбора даты")

    await clbck.message.answer("Выберите время события (например 13:30): ")
    await state.set_state(CreateEvent.enter_expires_time)


@router.message(CreateEvent.enter_expires_time, F.text)
async def expires_time_entered(msg: Message, state: FSMContext):
    is_correct_time: bool = validate_time_string(time_str=msg.text)
    if not is_correct_time:
        await msg.answer("Введите время в формате чч:мм, например 13:30")
        return
    hour, mitune = msg.text.split(":")
    await state.update_data(expire_time=time(int(hour), int(mitune)))
    await msg.answer(
        "За какое время прислать уведомление? ",
        reply_markup=get_keyboard(KeyboardType.SELECT_NOTIFY_TIMEOUT),
    )
    await state.set_state(CreateEvent.enter_notify)


@router.message(CreateEvent.enter_notify)
async def notify_timeout_entered(msg: Message, state: FSMContext):
    is_correct_time: bool = validate_time_string(time_str=msg.text)
    if not is_correct_time:
        await msg.answer("Введите время в формате чч:мм, например 13:30")
        return
    hour, mitune = msg.text.split(":")
    await state.update_data(notify_before=time(int(hour), int(mitune)))
    user_event_data = await state.get_data()

    event_data: EventForDB = tg_to_db_format(EventFromTelegramUser(**user_event_data))

    await msg.answer(
        st.event_show.format(
            title=event_data.title,
            description=event_data.description,
            expired_at=event_data.expired_at,
            notify_at=event_data.notify_at,
            created_at=dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            owner_id=event_data.owner_id,
        ),
        reply_markup=get_keyboard(KeyboardType.SAVE_EVENT),
    )
