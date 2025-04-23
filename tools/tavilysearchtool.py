import json
from typing import Any

from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from pydantic import BaseModel, ConfigDict

load_dotenv()
import os
tavily_api_key = os.getenv("TAVILY_API_KEY")

import logging
# Configure logging to capture DEBUG-level messages
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SearchDataFromTool(BaseModel):
    model_config = ConfigDict(extra='ignore')
    title:str
    url:str
    content:str
    score: float

def tavily_search(query: str, no_of_search_results: int) -> str:
    """
    Tool: Tavily Web Search

    Description:
    A tool that performs web searches using the Tavily Search API to retrieve current and relevant information from the internet.

    Parameters:
    - query (str): The search query or question to search for on the web
    - no_of_search_results (int): Number of search results to return (default: 5)

    Returns:
    A list of search results, where each result contains:
    - title: The title of the webpage or article
    - url: The webpage URL
    - content: The relevant content or snippet from the webpage
    - score: A relevancy score for the search result

    When to use:
    - Gathering current information from the web
    - Fact-checking or research tasks
    - Getting real-time updates on specific topics
    - Answering questions that require up-to-date information
    """
    logger.debug(f"query from llm was {query}")
    import time
    results = TavilySearchResults(
        max_results=no_of_search_results,
        tavily_api_key=tavily_api_key,
        include_answer=True,
        include_raw_content=True,
        include_images=False,
    ).invoke(query)
    time.sleep(1)
    results_ = [SearchDataFromTool(**item).model_dump() for item in results]
    dumps = json.dumps(results_)
    logger.debug(dumps)
    return dumps
