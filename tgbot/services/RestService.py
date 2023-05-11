from typing import Optional, List
from uuid import UUID

import aiohttp
from aiogram.types import User

from tgbot.config import Config
from tgbot.services.dto import UserFullDto
from tgbot.services.dto.request_object import RequestObject
from tgbot.services.dto.step_full_dto import StepFullDto
from tgbot.services.dto.user_configuration_dto import UserConfigurationDto
from tgbot.services.dto.user_configuration_full_dto import UserConfigurationFullDto


class RestService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RestService()
        return cls._instance

    def __init__(self):
        self._session = None
        self._config = Config.get_instance()

    async def _make_request(self, request_obj: RequestObject, is_json: bool = False):
        try:
            if not self._session:
                self._session = aiohttp.ClientSession()
            async with self._session.request(**request_obj.__dict__) as response:
                response.raise_for_status()
                if not is_json:
                    return await response.text()
                else:
                    return await response.json()
        except aiohttp.ClientResponseError as e:
            raise Exception(f"aiohttp client response error: {e}")
        except aiohttp.ClientError as e:
            raise Exception(f"aiohttp client error: {e}")
        except aiohttp.ServerDisconnectedError as e:
            raise Exception(f"aiohttp server disconnected error: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    async def current_user(self, user: User) -> UserFullDto:
        r = RequestObject(url=f'{self._config.api_base_url}/api/v1/private/users',
                          method='POST', data={
                'firstname': user.first_name,
                'lastname': user.last_name,
                'telegramId': user.id,
                'telegramUsername': user.username
            })
        response = await self._make_request(r, True)
        return UserFullDto(response)

    async def get_user_configuration(self, user_id: UUID) -> Optional[UserConfigurationFullDto]:
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/user_configurations',
            method='GET')
        try:
            response = await self._make_request(r, True)
        except:
            return None
        return UserConfigurationFullDto(response)

    async def get_all_user_configurations(self) -> List[UserConfigurationFullDto]:
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/user_configurations',
            method='GET')
        try:
            response = await self._make_request(r, True)
        except:
            return []
        return [UserConfigurationFullDto(payload) for payload in response]

    async def save_user_configuration(self, user_configuration_dto: UserConfigurationDto):
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/user_configurations',
            method='POST', data=user_configuration_dto.__dict__)
        await self._make_request(r, False)

    async def enable_user_configuration(self, user_id: UUID):
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/user_configurations/enable',
            method='PUT')
        await self._make_request(r)

    async def disable_user_configuration(self, user_id: UUID):
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/user_configurations/disable',
            method='PUT')
        await self._make_request(r)

    async def get_user_steps(self, user_id: UUID) -> List[StepFullDto]:
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/steps',
            method='GET')
        try:
            response = await self._make_request(r, True)
        except:
            return []
        return [StepFullDto(payload) for payload in response]

    async def grant_access_user(self, user_id: UUID, period: int):
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/grant_access/{period}',
            method='PUT')
        await self._make_request(r)

    async def revoke_access_user(self, user_id: UUID):
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/revoke_access',
            method='PUT')
        await self._make_request(r)

    async def promote_user(self, user_id: UUID):
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/promote',
            method='PUT')
        await self._make_request(r)

    async def demote_user(self, user_id: UUID):
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/{user_id}/demote',
            method='PUT')
        await self._make_request(r)

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[UserFullDto]:
        r = RequestObject(
            url=f'{self._config.api_base_url}/api/v1/private/users/getByTelegramId?telegramId={telegram_id}',
            method='GET')
        try:
            response = await self._make_request(r, True)
        except:
            return None
        return UserFullDto(response)
