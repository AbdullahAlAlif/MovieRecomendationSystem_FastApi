from fastapi import APIRouter, Query
from services.tmdb_service import search_movies

router = APIRouter(prefix="/tmdb", tags=["TMDB"])


@router.get("/search")
async def search(query: str = Query(...), page: int = 1):
    return await search_movies(query, page)
