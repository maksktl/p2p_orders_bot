from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class Config:
    db: DbConfig
    webapp_port: int


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        webapp_port=env.int('WEBAPP_PORT'),
    )
