from sqlalchemy import sql, Column, String, BIGINT

from tgbot.persistance.models import TimedBaseModel


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
