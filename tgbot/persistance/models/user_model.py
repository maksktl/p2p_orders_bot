from sqlalchemy import sql, Column, String, BIGINT

from tgbot.persistance.models import TimedBaseModel
from tgbot.services.dto import UserDto


class UserModel(TimedBaseModel):
    __tablename__ = 'user'
    query: sql.Select

    name = Column(String(64), nullable=False)
    surname = Column(String(64))
    middle_name = Column(String(64))
    email = Column(String(256))
    telegram_id = Column(BIGINT)
    telegram_url = Column(String)
    phone_number = Column(String(16))

    def __init__(self, user_dto: UserDto):
        self.name = user_dto.name
        self.surname = user_dto.surname
        self.middle_name = user_dto.middle_name
        self.email = user_dto.email
        self.telegram_id = user_dto.telegram_id
        self.telegram_url = user_dto.telegram_url
        self.phone_number = user_dto.phone_number

    def update(self, user_dto: UserDto):
        self.name = user_dto.name or self.name
        self.surname = user_dto.surname or self.surname
        self.middle_name = user_dto.middle_name or self.middle_name
        self.email = user_dto.email or self.email
        self.telegram_id = user_dto.telegram_id or self.telegram_id
        self.telegram_url = user_dto.telegram_url or self.telegram_url
        self.phone_number = user_dto.phone_number or self.phone_number