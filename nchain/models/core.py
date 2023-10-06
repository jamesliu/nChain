from pydantic import BaseModel
from typing import Optional, Dict, Any

class Chunk(BaseModel):
    id: int
    content: str

class Embedding(BaseModel):
    id: int
    vector: list[float]

class Entry(BaseModel):
    id: int
    score: Optional[float] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

