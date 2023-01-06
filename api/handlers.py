from typing import List

from fastapi import APIRouter, HTTPException

from api.external_service.client import MovieServiceError
from api.models.base import Movie
from api.movie_service.service import MovieService

movies = APIRouter()
service = MovieService()


# Search a movie in the external service
@movies.get('/movies/search', response_model=List[Movie])
async def search_movies(search: str):
    try:
        movie_list = await service.search_movies(search)
        return movie_list
    except MovieServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Get all favorite movies
@movies.get('/movies/favorites', response_model=List[Movie])
async def get_favorite_movies():
    return await service.get_favorite_movies()


# Add a movie to favorites
@movies.post('/movies/favorites')
async def add_favorite_movie(movie: Movie):
    await service.add_favorite_movie(movie)
    return {'message': 'Movie added to favorites'}


# Delete a movie from favorites
@movies.delete('/movies/favorites/{movie_id}')
async def delete_favorite_movie(movie_id: str):
    await service.delete_favorite_movie(movie_id)
    return {'message': 'Movie deleted from favorites'}
