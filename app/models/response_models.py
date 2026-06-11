from pydantic import BaseModel
from typing import List


class Citation(BaseModel):
    source: str
    chunk_id: str
    text: str


class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]