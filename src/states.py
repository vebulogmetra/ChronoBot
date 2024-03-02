from aiogram.fsm.state import (State, StatesGroup)


class CreateEvent(StatesGroup):
    enter_title = State()
    enter_description = State()
    enter_expires_date = State()
    enter_expires_time = State()
    enter_notify = State()
