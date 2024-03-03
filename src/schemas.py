from datetime import (date, datetime, time)

from pydantic import (BaseModel, ConfigDict)


class EventFromAPI(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    title: str
    description: str
    expired_at: str  # 2024-02-26 15:00:00
    notify_at: str  # 2024-02-26 13:30:00
    created_at: str  # 2024-02-21 18:24:54


class EventFromTelegramUser(BaseModel):
    owner_id: int
    title: str
    description: str
    expire_date: date
    expire_time: time
    notify_before: time


class EventForAPI(BaseModel):
    title: str
    description: str
    owner_id: int
    expired_at: str  # %Y-%m-%d %H:%M:%S
    notify_at: str  # %Y-%m-%d %H:%M:%S


class EventForDB(EventForAPI):
    expired_at: datetime
    notify_at: datetime


class UserBase(BaseModel):
    id: int


class UserForDB(UserBase): ...
