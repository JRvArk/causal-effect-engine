from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Causal Effect Engine", version="0.1.0")


class EffectRequest(BaseModel):
    dataset: str
    treatment: str
    outcome: str
    covariates: list[str]
    estimator: str = "dml"


class EffectResponse(BaseModel):
    estimator: str
    ate: float
    se: float
    ci_lower: float
    ci_upper: float


class RecommendRequest(BaseModel):
    dataset: str
    treatment: str
    outcome: str
    covariates: list[str]
    top_k: int = 100


class RecommendResponse(BaseModel):
    unit_ids: list[int]
    uplift_scores: list[float]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/effect", response_model=EffectResponse)
def estimate_effect(req: EffectRequest):
    raise NotImplementedError


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    raise NotImplementedError
