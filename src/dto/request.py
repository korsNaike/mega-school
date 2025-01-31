from typing import List

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    id: int
    query: str


class PredictionResponse(BaseModel):
    id: int
    answer: int
    reasoning: str
    sources: List[str]

class ResponseFromAgent(BaseModel):
    answer: int
    reasoning: str
