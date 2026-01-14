from fastapi import APIRouter, Query
from services.tfidf_service import recommend_tfidf

router = APIRouter(prefix="/recommend", tags=["Recommendations"])


@router.get("/tfidf")
def tfidf(title: str = Query(...), top_n: int = 10):
    return recommend_tfidf(title, top_n)
