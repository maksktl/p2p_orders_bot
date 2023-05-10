from dataclasses import dataclass

from environs import Env

@dataclass
class TgBot:
    token: str
    use_redis: bool
    webapp_url: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    _instance = None

    tg_bot: TgBot
    misc: Miscellaneous
    webapp_port: int
    provider_token: str
    api_base_url: str

    @classmethod
    def get_instance(cls, path: str = None):
        if cls._instance is None:
            env = Env()
            env.read_env(path)
            cls._instance = Config(
                tg_bot=TgBot(
                    token=env.str("BOT_TOKEN"),
                    use_redis=env.bool("USE_REDIS"),
                    webapp_url=env.str("WEBAPP_URL"),
                ),
                misc=Miscellaneous(),
                webapp_port=env.int("WEBAPP_PORT"),
                provider_token=env.str("PROVIDER_TOKEN"),
                api_base_url=env.str("API_BASE_URL")
            )
        return cls._instance
