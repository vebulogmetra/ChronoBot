from abc import ABC, abstractmethod
from enum import Enum

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class KeyboardFactory(ABC):
    @abstractmethod
    def create_keyboard(self):
        pass


class Menu(KeyboardFactory):
    def create_keyboard(self) -> InlineKeyboardMarkup:
        menu_kb = [
            [
                InlineKeyboardButton(
                    text="📝 Создать новое событие", callback_data="create_event"
                ),
                InlineKeyboardButton(
                    text="📄 Прислать список все событий",
                    callback_data="fetch_user_events",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔎 Прислать список событий на сегоня",
                    callback_data="fetch_user_today_events",
                )
            ],
        ]
        menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_kb)

        return menu_keyboard


class AdminMenu(KeyboardFactory):
    def create_keyboard(self) -> InlineKeyboardMarkup:
        admin_menu_kb = [
            [
                InlineKeyboardButton(
                    text="📝 Создать событие", callback_data="create_event"
                ),
                InlineKeyboardButton(
                    text="📄 Мои события",
                    callback_data="fetch_user_events",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔎 Мои события на сегодня",
                    callback_data="fetch_user_today_events",
                ),
                InlineKeyboardButton(
                    text="🔌 Uptime info",
                    callback_data="uptime_info",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="👥 Все пользователи",
                    callback_data="fetch_all_users",
                ),
                InlineKeyboardButton(
                    text="📔 Все события",
                    callback_data="fetch_all_events",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⌚️ Все задания (cron)",
                    callback_data="show_cronjobs",
                ),
            ],
        ]
        admin_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=admin_menu_kb)

        return admin_menu_keyboard


class Exit(KeyboardFactory):
    def create_keyboard(self) -> ReplyKeyboardMarkup:
        exit_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True
        )
        return exit_kb


class BackStep(KeyboardFactory):
    def create_keyboard(self) -> ReplyKeyboardMarkup:
        backstep_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Назад")]], resize_keyboard=True
        )
        return backstep_kb


class SelectNotifyTimeout(KeyboardFactory):
    def create_keyboard(self):
        notify_kb = [
            [
                KeyboardButton(text="00:30"),
                KeyboardButton(text="1:00"),
                KeyboardButton(text="1:30"),
            ],
            [
                KeyboardButton(text="2:00"),
                KeyboardButton(text="2:30"),
                KeyboardButton(text="3:00"),
            ],
        ]
        notify_keyboard = ReplyKeyboardMarkup(
            keyboard=notify_kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите способ взаимодействия",
        )

        return notify_keyboard


class SendEvent(KeyboardFactory):
    def create_keyboard(self) -> InlineKeyboardMarkup:
        send_event_kb = [
            [
                InlineKeyboardButton(
                    text="🚀 Отправить событие", callback_data="send_event"
                ),
            ],
        ]
        send_event_keyboard = InlineKeyboardMarkup(inline_keyboard=send_event_kb)

        return send_event_keyboard


class SaveEvent(KeyboardFactory):
    def create_keyboard(self) -> InlineKeyboardMarkup:
        send_event_kb = [
            [
                InlineKeyboardButton(text="💾 Сохранить", callback_data="save_event"),
            ],
        ]
        save_event_keyboard = InlineKeyboardMarkup(inline_keyboard=send_event_kb)

        return save_event_keyboard


class KeyboardType(Enum):
    ADMIN_MENU = AdminMenu
    MENU = Menu
    BACKSTEP = BackStep
    EXIT = Exit
    SELECT_NOTIFY_TIMEOUT = SelectNotifyTimeout
    SEND_EVENT = SendEvent
    SAVE_EVENT = SaveEvent


def get_keyboard(type: KeyboardType):
    return type.value().create_keyboard()


def get_remove_keyboard(cb_data: str) -> InlineKeyboardMarkup:
    remove_kb = [
        [
            InlineKeyboardButton(text="❌ Удалить", callback_data=cb_data),
        ],
    ]
    remove_keyboard = InlineKeyboardMarkup(inline_keyboard=remove_kb)

    return remove_keyboard
