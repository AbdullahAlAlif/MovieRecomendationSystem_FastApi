from typing import Optional, List
from pydantic import BaseModel


class TMDBMovieCard(BaseModel):
    tmdb_id: int
    title: str
    poster_url: Optional[str]
    release_date: Optional[str]
    vote_average: Optional[float]


class TMDBMovieDetails(BaseModel):
    tmdb_id: int
    title: str
    overview: Optional[str]
    release_date: Optional[str]
    poster_url: Optional[str]
    backdrop_url: Optional[str]
    genres: List[dict] = []


class TFIDFRecItem(BaseModel):
    title: str
    score: float
    tmdb: Optional[TMDBMovieCard]


class SearchBundleResponse(BaseModel):
    query: str
    movie_details: TMDBMovieDetails
    tfidf_recommendations: List[TFIDFRecItem]
    genre_recommendations: List[TMDBMovieCard]
