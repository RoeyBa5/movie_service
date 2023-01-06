import asyncio
import logging
from typing import Optional, List

from aiohttp import ClientSession, ClientResponseError
from tenacity import retry, stop_after_attempt, wait_incrementing, retry_if_exception_type

from api.external_service.config import ClientConfig
from api.models.base import Movie
from api.models.external import SearchMovies

client_config = ClientConfig(base_url='http://www.omdbapi.com/', timeout=10, api_key='e6f034a9')


class MovieServiceError(Exception):
    pass


class MovieClient:
    def __init__(self, config: ClientConfig = client_config):
        self._config = config

    async def search_movies(self, search: str) -> List[Movie]:
        path = ''
        params = {'s': search}
        response = await self._request(method='GET', path=path, params=params)
        search_movies = SearchMovies.from_dict(response)
        if search_movies.Error:
            raise MovieServiceError(search_movies.Error)
        return (SearchMovies.from_dict(response)).Search

    @retry(stop=stop_after_attempt(3), wait=wait_incrementing(increment=3, max=30),
           retry=retry_if_exception_type(asyncio.TimeoutError))
    async def _request(self,
                       method: str,
                       path: str,
                       params: Optional[dict] = None,
                       data: Optional[dict] = None) -> dict:
        async with ClientSession() as client:
            url = f'{self._config.base_url}{path}'
            params.update({'apikey': self._config.api_key})
            response = await client.request(method=method, url=url, params=params, data=data,
                                            timeout=self._config.timeout)
            return await self._handle_response(response)

    @staticmethod
    async def _handle_response(resp) -> dict:
        if resp.status >= 300:
            response = await resp.text()
            logging.warning(f'Request failed, got response: {response}', extra={'url': resp.url, 'status:': resp.status,
                                                                                'reason': resp.reason})
            raise ClientResponseError(resp.request_info, resp.history, status=resp.status, message=resp.reason)
        return await resp.json()
