# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import wikipedia
import time

# To run this file, you'll need the following libraries.
# You can install them with pip:
# pip install fastapi "uvicorn[standard]" pydantic wikipedia transformers torch

# Initialize FastAPI with a title for the API documentation
app = FastAPI(title="AI Research Agent Backend")

# Initialize Hugging Face summarizer pipeline.
# Note: The first time you run this, it will download a large model (around 1GB).
# This process might take a few minutes.
# device=-1 means it will run on the CPU, which is slower but more compatible.
print("Initializing Hugging Face summarization model. This may take a moment...")
try:
    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        device=-1  # Use CPU
    )
    print("Model initialized successfully.")
except Exception as e:
    # A robust way to handle model initialization failure if the file is run in a limited environment
    print(f"Failed to initialize Hugging Face model: {e}")
    summarizer = None


def summarize_content(texts):
    """
    Combines and summarizes a list of text strings.
    """
    # Join all non-empty text strings into a single large string
    combined_text = " ".join([t for t in texts if t and t.strip()])
    
    if not combined_text:
        return "No content available to summarize."
    
    # The key fix: add 'truncation=True'. Without this, the summarizer will
    # crash if the combined text from Wikipedia exceeds its maximum input length.
    # It automatically truncates the input to fit the model's token limit.
    try:
        summary = summarizer(
            combined_text, 
            max_length=150, 
            min_length=50, 
            truncation=True
        )
        return summary[0]["summary_text"]
    except Exception as e:
        print(f"Summarization failed: {e}")
        return "An error occurred during summarization."


# ---------------------------------------------
# Wikipedia search and content extraction
# ---------------------------------------------

def web_search(query, num_results=3, retries=3):
    """
    Searches Wikipedia for a query with built-in retry logic.
    """
    for attempt in range(retries):
        try:
            return wikipedia.search(query, results=num_results)
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)  # wait 1 second before retrying
                continue
            else:
                print(f"Wikipedia search failed after {retries} attempts for query: '{query}'")
                return []

def extract_content(page_title, retries=3):
    """
    Extracts content from a Wikipedia page with built-in retry logic.
    Handles common Wikipedia library errors like PageError and DisambiguationError.
    """
    for attempt in range(retries):
        try:
            page = wikipedia.page(page_title, auto_suggest=False, redirect=True)
            return {
                "title": page.title,
                "url": page.url,
                "text": page.content
            }
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
            # These are common errors, we just skip the page.
            print(f"Skipping page '{page_title}' due to error: {e}")
            return {"title": page_title, "url": "", "text": "Content not available."}
        except Exception as e:
            # Catch all other exceptions and retry if possible.
            if attempt < retries - 1:
                time.sleep(1)
                continue
            else:
                print(f"Failed to extract content for '{page_title}' after {retries} attempts.")
                return {"title": page_title, "url": "", "text": ""}


# Pydantic model for the research request
class ResearchRequest(BaseModel):
    query: str
    num_results: int = 3
    summary_type: str = "paragraph" # This field is not used in the current logic but is good to have.

# Root endpoint for a simple health check
@app.get("/")
def root():
    return {"message": "AI Research Agent is running 🚀"}

# Main research endpoint that handles the workflow
@app.post("/research/research")
async def research_endpoint(request: ResearchRequest):
    if not summarizer:
        return {"error": "Summarization model not loaded. Check the server logs for details."}

    try:
        # Step 1: Search Wikipedia for page titles
        titles = web_search(request.query, num_results=request.num_results)
        
        # Step 2: Extract content from each page
        contents = [extract_content(title) for title in titles]

        # Step 3: Filter out pages that didn't provide any text
        valid_contents = [c for c in contents if c.get("text") and c["text"] != "Content not available."]
        texts = [c["text"] for c in valid_contents]
        
        # Step 4: Summarize the combined content
        summary = summarize_content(texts)

        # Step 5: Return the summary and sources
        return {
            "query": request.query,
            "summary": summary,
            "sources": [{"title": c["title"], "url": c["url"]} for c in valid_contents]
        }

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}
