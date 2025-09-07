from pydantic import BaseModel

class ResearchRequest(BaseModel):
    query: str
    num_results: int = 5   # default value
    summary_type: str = "bullet"  # could be "bullet" or "paragraph"
