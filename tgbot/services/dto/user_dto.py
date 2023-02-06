from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserDto:
    id: UUID
    name: str
    surname: str
    middle_name: str
    email: str
    telegram_id: int
    telegram_url: str
    phone_number: str
