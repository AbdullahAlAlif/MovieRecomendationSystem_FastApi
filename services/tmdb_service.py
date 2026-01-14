import httpx
from fastapi import HTTPException
from typing import Dict, Any, List

from core.config import TMDB_API_KEY, TMDB_BASE, TMDB_IMG_500
from models.schemas import TMDBMovieCard, TMDBMovieDetails


def img_url(path: str | None):
    if not path:
        return None
    return f"{TMDB_IMG_500}{path}"


async def tmdb_get(path: str, params: Dict[str, Any]):
    params["api_key"] = TMDB_API_KEY

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{TMDB_BASE}{path}", params=params)

    if r.status_code != 200:
        raise HTTPException(502, r.text)

    return r.json()


async def search_movies(query: str, page: int = 1):
    return await tmdb_get("/search/movie", {
        "query": query,
        "include_adult": False,
        "language": "en-US",
        "page": page
    })


async def movie_details(movie_id: int) -> TMDBMovieDetails:
    data = await tmdb_get(f"/movie/{movie_id}", {"language": "en-US"})
    return TMDBMovieDetails(
        tmdb_id=data["id"],
        title=data["title"],
        overview=data.get("overview"),
        release_date=data.get("release_date"),
        poster_url=img_url(data.get("poster_path")),
        backdrop_url=img_url(data.get("backdrop_path")),
        genres=data.get("genres", [])
    )


def to_cards(results: List[dict], limit: int):
    return [
        TMDBMovieCard(
            tmdb_id=m["id"],
            title=m.get("title", ""),
            poster_url=img_url(m.get("poster_path")),
            release_date=m.get("release_date"),
            vote_average=m.get("vote_average")
        )
        for m in results[:limit]
    ]


async def recommend_by_genre(tmdb_id: int, limit: int = 12) -> List[TMDBMovieCard]:
    # 1. Get the original movie to extract genres
    movie = await movie_details(tmdb_id)
    
    if not movie.genres:
        return []

    # 2. Get genre IDs 
    genre_ids = [g["id"] for g in movie.genres]
    genre_ids_str = ",".join(str(gid) for gid in genre_ids)

    # 3. Search TMDB for movies with these genres
    # Note: TMDB's discover endpoint allows filtering by genre
    params = {
        "with_genres": genre_ids_str,
        "sort_by": "popularity.desc",
        "include_adult": False,
        "language": "en-US",
        "page": 1,
        "vote_count.gte": 10,  # avoid obscure movies
    }

    data = await tmdb_get("/discover/movie", params)
    results = data.get("results", [])

    # 4. Remove the original movie from results (if present)
    filtered = [m for m in results if m.get("id") != tmdb_id]

    # 5. Convert to cards and limit
    return to_cards(filtered, limit)