from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserFullDto:
    id: UUID
    name: str
    surname: str
    middle_name: str
    email: str
    telegram_id: int
    telegram_url: str
    phone_number: str

    def __init__(self, model):
        self.id = model.id
        self.name = model.name
        self.surname = model.name
        self.middle_name = model.middle_name
        self.email = model.email
        self.telegram_id = model.telegram_id
        self.telegram_url = model.telegram_url
        self.phone_number = model.phone_number
