from typing import Any, Self
from pandas import DataFrame
from httpx import Response
from httpx._types import QueryParamTypes
import tomllib
import pandas as pd
from platformdirs import user_config_path
from pathlib import Path

from ..common.pandas_utils import crop_by_interval
from .outlet.outlet_sync_client import OutletSyncClient
from .platform.platform_sync_client import PlatformSyncClient

from ..common.exceptions import ClientException
from .api_query import Query, ProviderType

_client_instance = None


class PvradarClient:
    def __init__(
        self,
        outlet_base_url: str = '',
        outlet_token: str = '',
        platform_base_url: str = '',
        platform_username: str = '',
        platform_password: str = '',
        platform_token: str = '',
    ):
        self._outlet_base_url = outlet_base_url
        self._outlet_token = outlet_token

        self._platform_base_url = platform_base_url
        self._platform_username = platform_username
        self._platform_password = platform_password
        self._platform_token = platform_token

        self._outlet_client = None
        self._platform_client = None

    def __repr__(self) -> str:
        return f'<PvradarClient outlet={self._outlet_base_url} platform={self._platform_base_url}>'

    def _guess_provider(self, query: Query | str) -> ProviderType:
        path = query
        if isinstance(query, Query):
            if query.provider:
                return query.provider
            if query.project_id:
                return 'platform'
            path = query.path
        if 'assemblies' in path:
            return 'platform'
        return 'outlet'

    def _get_outlet_client(self) -> OutletSyncClient:
        if isinstance(self._outlet_client, OutletSyncClient):
            return self._outlet_client
        c = OutletSyncClient.instance(
            token=self._outlet_token,
            base_url=self._outlet_base_url,
        )
        self._outlet_client = c
        return c

    def _get_platform_client(self) -> PlatformSyncClient:
        if isinstance(self._platform_client, PlatformSyncClient):
            return self._platform_client
        c = PlatformSyncClient.instance(
            base_url=self._platform_base_url,
            username=self._platform_username,
            password=self._platform_password,
            token=self._platform_token,
        )
        self._outlet_client = c
        return c

    def _subclient(self, query: Query | str) -> OutletSyncClient | PlatformSyncClient:
        provider = self._guess_provider(query)
        if provider == 'outlet':
            return self._get_outlet_client()
        else:
            return self._get_platform_client()

    def get(self, query: str | Query, params: QueryParamTypes | None = None) -> Response:
        return self._subclient(query).get(query, params)

    def get_csv(self, query: str | Query, params: QueryParamTypes | None = None) -> str:
        return self._subclient(query).get_csv(query=query, params=params)

    def get_json(self, query: str | Query, params: QueryParamTypes | None = None) -> Any:
        return self._subclient(query).get_json(query=query, params=params)

    def get_df(
        self,
        query: str | Query,
        *,
        params: QueryParamTypes | None = None,
        crop_interval: pd.Interval | None = None,
    ) -> DataFrame:
        result = self._subclient(query).get_df(query=query, params=params)
        if crop_interval:
            result = crop_by_interval(result, crop_interval)
        return result

    @classmethod
    def from_config(cls, config_path_str='') -> Self:
        if not config_path_str:
            config_path = user_config_path('pvradar') / 'sdk.toml'
        else:
            config_path = Path(config_path_str)
        try:
            with config_path.open('rb') as conf_file:
                values = tomllib.load(conf_file)
                if 'base_url' in values:
                    values['outlet_base_url'] = values['base_url']
                if 'token' in values:
                    values['outlet_token'] = values['token']
                    values['platform_token'] = values['token']
            return cls(
                outlet_base_url=values.get('outlet_base_url', 'https://api.pvradar.com/v2'),
                outlet_token=values.get('outlet_token', ''),
                platform_base_url=values.get('platform_base_url', 'https://platform.pvradar.com/api'),
                platform_username=values.get('platform_username', ''),
                platform_password=values.get('platform_password', ''),
                platform_token=values.get('platform_token', ''),
            )
        except OSError:
            raise ClientException(
                f'CRITICAL: No config found, expected file: {config_path} . '
                + 'Please contact PVRADAR tech. support if unsure what it is.'
            )
        except tomllib.TOMLDecodeError:
            raise ClientException(
                f'CRITICAL: Invalid config format found in file: {config_path} .' + 'Please contact PVRADAR tech. support.'
            )
        except KeyError as key:
            raise ClientException(
                f'Config key: {key} was not found',
            )

    @classmethod
    def instance(cls) -> Self:
        global _client_instance
        if not _client_instance:
            _client_instance = cls.from_config()
        return _client_instance
