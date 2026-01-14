import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY missing in .env")

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_500 = "https://image.tmdb.org/t/p/w500"

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PICKLE_DIR = os.path.join(BASE_DIR, "pickle Files")

DF_PATH = os.path.join(PICKLE_DIR, "df.pkl")
INDICES_PATH = os.path.join(PICKLE_DIR, "indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(PICKLE_DIR, "tfidf_matrix.pkl")
TFIDF_PATH = os.path.join(PICKLE_DIR, "tfidf.pkl")
