from fastapi import APIRouter, Query 
from services.tmdb_service import movie_details, recommend_by_genre

router = APIRouter(prefix="/movie", tags=["Movie"])


@router.get("/id/{tmdb_id}")
async def details(tmdb_id: int):
    return await movie_details(tmdb_id)


@router.get("/recommend/genre/{tmdb_id}")
async def recommend_genre(tmdb_id: int, limit: int = Query(12, ge=1, le=20)):
    """
    Get genre-based recommendations for a movie by its TMDB ID.
    """
    try:
        return await recommend_by_genre(tmdb_id, limit=limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Recommendation failed: {str(e)}")