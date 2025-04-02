import requests
import time
from src.tools.toolClassDecorator import tool

@tool(
    name="wiki_search_tool",
    description="Search for a Wikipedia article.",
    args=[("query", "str")],
    outputs="dict"
)
def wikipedia_search_tool(query):
    formatted_query = query.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_query}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = {
            "title": data.get("title"),
            "extract": data.get("extract"),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page")
        }
        return result
    else:
        return {"error": f"Article not found or error occurred: {response.status_code}"}
