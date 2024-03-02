# Телеграм бот для напоминаний о событиях

Этот телеграм бот позволяет пользователям создавать напоминания о событиях и получать уведомления в указанное время.

## Требования
- Python 3.6+

## Установка
1. Клонируйте репозиторий: `git clone https://github.com/your/repository.git`
2. Перейдите в каталог с проектом: `cd reminder_bot`
3. Установите зависимости: `pip install -r requirements.txt`

## Конфигурация
1. Получите токен для своего телеграм бота через BotFather и добавьте его в коде в переменную `BOT_TOKEN`.
2. Опционально: можно изменить настройки базы данных и другие параметры в соответствии с собственными потребностями.

## Запуск
Запустите бота командой `python src/main.py`.

## Использование
После запуска бота, вы можете взаимодействовать с ним следуя инструкциям:
- Используйте `/start` чтобы начать общение с ботом.
- Следуйте инструкциям

## Дополнительная информация
Данный проект использует библиотеки aiogram 3 для работы с телеграм API, также APScheduler для планирования задач, SQLAlchemy, aiosqlite - для работы с базой данных SQLite.
