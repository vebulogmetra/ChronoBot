from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.crud import create_user, get_user_by_id
from kb import KeyboardType, get_keyboard
from res import strings as st
from states import CreateEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from schemas import UserForDB
from settings import ADMIN_ID

router = Router()


@router.message(F.text, Command("start"))
async def cmd_start_handler(msg: Message, db_session: AsyncSession):
    current_user = await get_user_by_id(db_session=db_session, user_id=msg.from_user.id)
    if current_user is None:
        await create_user(db_session=db_session, user_data=UserForDB(id=msg.from_user.id))
    await msg.answer(
        st.greet.format(name=msg.from_user.username),
        reply_markup=get_keyboard(KeyboardType.MENU),
    )


@router.message(F.text, Command("admin"))
async def cmd_admin_handler(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer(st.admin_only, reply_markup=get_keyboard(KeyboardType.MENU))
    else:
        await msg.answer(
            "Расширенное меню:", reply_markup=get_keyboard(KeyboardType.ADMIN_MENU)
        )


@router.message(F.text, Command("registration"))
async def cmd_registration_user_handler(msg: Message, db_session: AsyncSession):
    user = await get_user_by_id(db_session=db_session, user_id=msg.from_user.id)
    if user is not None:
        await msg.answer(
            "Я уже знаю Вас. Регистрация не требуется",
            reply_markup=get_keyboard(KeyboardType.MENU),
        )
        return
    await create_user(db_session=db_session, user_data=UserForDB(id=msg.from_user.id))
    await msg.answer(
        "Вы успешно зарегистрированы!",
        reply_markup=get_keyboard(KeyboardType.MENU),
    )


@router.message(F.text == "◀️ Выйти в меню")
@router.message(StateFilter("*"), Command("cancel"))
async def cmd_cancel_handler(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await msg.answer(st.menu, reply_markup=get_keyboard(KeyboardType.MENU))


@router.message(F.text == "Назад")
@router.message(StateFilter("*"), Command("back"))
async def cmd_backstep_handler(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == CreateEvent.enter_title:
        await msg.answer("Вы на первом шаге. Введите название события.")
        return

    prev = None
    for step in CreateEvent.__all_states__:
        if step.state == current_state:
            await state.set_state(prev)
            await msg.answer(f"Возврат.")
            return
        prev = step
