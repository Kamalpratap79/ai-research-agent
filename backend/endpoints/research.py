from fastapi import APIRouter
from ..models.request import ResearchRequest
from ..models.response import ResearchResponse
from ..services.search import web_search
from ..services.extract import extract_content
from ..services.summarize import summarize_content

router = APIRouter(prefix="/research", tags=["Research"])

@router.post("/research", response_model=ResearchResponse)
def research_endpoint(request: ResearchRequest):
    try:
        # 1. Perform Web Search
        urls = web_search(request.query, request.num_results)

        # 2. Extract content from URLs
        extracted_data = extract_content(urls)

        # 3. Summarize using LLM
        summary = summarize_content(extracted_data, request.summary_type)

        return {
            "query": request.query,
            "summary": summary,
            "sources": extracted_data  # this must match the Source model
        }
    except Exception as e:
        return {"error": str(e)}

