from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    id: int

class QueryResponse(BaseModel):
    id: int
    answer: Optional[int]
    reasoning: str
    sources: List[str]
