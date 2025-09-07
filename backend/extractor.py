import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return " ".join(paragraphs[:5])  # take first 5 paragraphs
    except Exception as e:
        return f"Error extracting {url}: {e}"
