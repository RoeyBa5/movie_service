from typing import List

from pymongo import MongoClient

from api.models.base import Movie

COLLECTION_NAME = 'favorites'

DB_NAME = 'movies'

DB_HOST = "mongodb://localhost:27017/"


class DBManager:
    def __init__(self, client: MongoClient = MongoClient(DB_HOST)):
        self._client = client
        self._db = self._client[DB_NAME]
        self._collection = self._db[COLLECTION_NAME]

    def get_all(self) -> List[Movie]:
        movies = [res for res in self._collection.find()]
        return [Movie.from_dict(movie) for movie in movies]

    def insert(self, movie: Movie):
        self._collection.insert_one(movie.to_dict())

    def delete(self, movie_id: str):
        self._collection.delete_one({"imdbID": movie_id})
