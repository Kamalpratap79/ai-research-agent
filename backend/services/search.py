import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def web_search(query: str, num_results: int = 5):
    """
    Example using SerpAPI
    """
    url = f"https://serpapi.com/search.json?q={query}&num={num_results}&api_key={SERPAPI_KEY}"
    response = requests.get(url)
    results = response.json().get("organic_results", [])
    urls = [r.get('link') for r in results[:num_results]]

    return urls
