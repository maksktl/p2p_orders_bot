from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserDto:
    id: UUID = None
    name: str = None
    surname: str = None
    middle_name: str = None
    email: str = None
    telegram_id: int = None
    telegram_url: str = None
    phone_number: str = None
    bot_access: bool = None
    admin: bool = None

    def fill_from_user(self, user):
        self.name = user.first_name
        self.surname = user.last_name
        self.telegram_id = user.id
        self.telegram_url = user.get_mention(user.full_name)
