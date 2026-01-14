import pickle
import numpy as np
import pandas as pd
from fastapi import HTTPException
from typing import Dict, List, Tuple

from core.config import DF_PATH, INDICES_PATH, TFIDF_MATRIX_PATH


df = None
tfidf_matrix = None
TITLE_TO_IDX: Dict[str, int] = {}


def _norm(title: str) -> str:
    return title.strip().lower()


def init_tfidf():
    global df, tfidf_matrix, TITLE_TO_IDX

    with open(DF_PATH, "rb") as f:
        df = pickle.load(f)

    with open(INDICES_PATH, "rb") as f:
        indices = pickle.load(f)

    with open(TFIDF_MATRIX_PATH, "rb") as f:
        tfidf_matrix = pickle.load(f)

    TITLE_TO_IDX = {_norm(k): int(v) for k, v in indices.items()}


def recommend_tfidf(title: str, top_n: int) -> List[Tuple[str, float]]:
    key = _norm(title)

    if key not in TITLE_TO_IDX:
        raise HTTPException(404, f"Title not found: {title}")

    idx = TITLE_TO_IDX[key]
    scores = (tfidf_matrix @ tfidf_matrix[idx].T).toarray().ravel()
    order = np.argsort(-scores)

    results = []
    for i in order:
        if i == idx:
            continue
        results.append((df.iloc[i]["title"], float(scores[i])))
        if len(results) >= top_n:
            break

    return results
