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
