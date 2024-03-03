from datetime import (datetime, timedelta)

from schemas import (EventForAPI, EventForDB, EventFromTelegramUser)


def tg_to_api_format(event_data: EventFromTelegramUser) -> EventForAPI:
    expired_at = datetime.combine(event_data.expire_date, event_data.expire_time)
    notify_at = expired_at - timedelta(
        hours=event_data.notify_before.hour, minutes=event_data.notify_before.minute
    )

    output_data: EventForAPI = EventForAPI(
        title=event_data.title,
        description=event_data.description,
        owner_id=event_data.owner_id,
        expired_at=expired_at.strftime("%Y-%m-%d %H:%M:%S"),
        notify_at=notify_at.strftime("%Y-%m-%d %H:%M:%S"),
    )

    return output_data


def tg_to_db_format(event_data: EventFromTelegramUser) -> EventForDB:
    expired_at = datetime.combine(event_data.expire_date, event_data.expire_time)
    notify_at = expired_at - timedelta(
        hours=event_data.notify_before.hour, minutes=event_data.notify_before.minute
    )

    output_data: EventForDB = EventForDB(
        title=event_data.title,
        description=event_data.description,
        owner_id=event_data.owner_id,
        expired_at=expired_at,
        notify_at=notify_at,
    )

    return output_data


def db_to_tg_format(event_data) -> EventForDB:
    expired_at = datetime.strptime(event_data.expired_at, "%Y-%m-%d %H:%M:%S")
    notify_at = datetime.strptime(event_data.notify_at, "%Y-%m-%d %H:%M:%S")

    output_data: EventForDB = EventForDB(
        title=event_data.title,
        description=event_data.description,
        owner_id=event_data.owner_id,
        expired_at=expired_at,
        notify_at=notify_at,
    )

    return output_data
