from src.Agent import Agent
from src.tools.wikipedia_search_tool import tool, wikipedia_search_tool
from src.tools.duck_duck_go import tool, duck_duck_go_search_tool

import time
import requests
if __name__ == "__main__":
    agent = Agent(
        tools=[wikipedia_search_tool, duck_duck_go_search_tool], 
        groq_model_name="llama-3.3-70b-versatile"
        );
    agent("Who will face off in the 2025 Copa del Rey final?", max_iterations=10);