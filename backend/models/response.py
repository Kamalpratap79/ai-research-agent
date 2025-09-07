from pydantic import BaseModel
from typing import List, Optional

class Source(BaseModel):
    title: Optional[str]
    url: str
    date: Optional[str]
    text: Optional[str]

class ResearchResponse(BaseModel):
    query: str
    summary: str
    sources: List[Source]
