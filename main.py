from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.startup import load_pickles
from routes import home, tmdb, recommend, movie



app = FastAPI(title="Movie Recommendation System", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["movierecomendationsystemfastapi.streamlit.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    load_pickles()


app.include_router(home.router)
app.include_router(tmdb.router)
app.include_router(recommend.router)
app.include_router(movie.router)


@app.get("/health")
def health():
    return {"status": "ok"}

