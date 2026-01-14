from fastapi import APIRouter, Query
from services.tmdb_service import tmdb_get, to_cards

router = APIRouter(prefix="/home", tags=["Home"])


@router.get("/")
async def home(category: str = "popular", limit: int = Query(24, le=50)):
    if category == "trending":
        data = await tmdb_get("/trending/movie/day", {})
    else:
        data = await tmdb_get(f"/movie/{category}", {"page": 1})

    return to_cards(data.get("results", []), limit)
