from typing import List

from api.db.db_manager import DBManager
from api.external_service.client import MovieClient
from api.models.base import Movie


class MovieService:
    def __init__(self, client: MovieClient = MovieClient(), db: DBManager = DBManager()):
        self._client = client
        self._db = db

    async def search_movies(self, search: str) -> List[Movie]:
        return await self._client.search_movies(search)

    async def get_favorite_movies(self) -> List[Movie]:
        return self._db.get_all()

    async def add_favorite_movie(self, movie: Movie):
        self._db.insert(movie)

    async def delete_favorite_movie(self, movie_id: str):
        self._db.delete(movie_id)
