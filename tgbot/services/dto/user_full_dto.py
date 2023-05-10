from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserFullDto:
    id: UUID
    firstname: str
    lastname: str
    telegram_id: int
    telegram_username: str
    bot_access: bool
    admin: bool

    def __init__(self, payload: dict):
        self.id = payload.get('id', None)
        self.name = payload.get('firstname', None)
        self.surname = payload.get('lastname', None)
        self.telegram_id = payload.get('telegramId', None)
        self.bot_access = payload.get('botAccess', False)
        self.admin = payload.get('admin', False)
