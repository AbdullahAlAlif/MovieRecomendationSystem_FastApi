from fastapi import APIRouter
from services.tmdb_service import movie_details

router = APIRouter(prefix="/movie", tags=["Movie"])


@router.get("/id/{tmdb_id}")
async def details(tmdb_id: int):
    return await movie_details(tmdb_id)
