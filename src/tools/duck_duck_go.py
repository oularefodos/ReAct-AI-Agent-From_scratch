import requests
import time
from src.tools.toolClassDecorator import tool
from duckduckgo_search import DDGS

@tool(
    name="duckduckgo_search",
    description="make a serach on duckduckgo and return 5 results",
    args=[("query", "str")],
    outputs="dict"
)
def duck_duck_go_search_tool(query):
    ddgs = DDGS()
    result = ddgs.text(query, max_results=5)
    return result