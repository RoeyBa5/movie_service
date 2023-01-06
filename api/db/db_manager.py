from typing import List

from pymongo import MongoClient

from api.db.config import MongoConfig
from api.models.base import Movie

DB_HOST = "mongodb://localhost:27017/"
DB_NAME = 'movies'
COLLECTION_NAME = 'favorites'
mongo_config = MongoConfig(host=DB_HOST, db_name=DB_NAME, collection_name=COLLECTION_NAME)


class DBManager:
    def __init__(self, client: MongoClient = MongoClient(mongo_config.host)):
        self._client = client
        self._db = self._client[mongo_config.db_name]
        self._collection = self._db[mongo_config.collection_name]

    def get_all(self) -> List[Movie]:
        movies = [res for res in self._collection.find()]
        return [Movie.from_dict(movie) for movie in movies]

    def insert(self, movie: Movie):
        self._collection.insert_one(movie.to_dict())

    def delete(self, movie_id: str):
        self._collection.delete_one({"imdbID": movie_id})
