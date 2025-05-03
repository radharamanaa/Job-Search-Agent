import json

from langchain_google_community import GoogleSearchAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentType
from dotenv import load_dotenv
# Step 1: Set up the Google Search API Wrapper
# Ensure environment variables are set for Google API
# export GOOGLE_API_KEY='your-api-key'
# export GOOGLE_CSE_ID='your-cse-id'
load_dotenv()
google_search_var = GoogleSearchAPIWrapper(k=10)

def google_search(query: str) -> str:
    """
    Performs a Google search using the Custom Search API and returns relevant search results.
    This tool is designed for retrieving current information from the web through Google Search.

    The function executes a search query and returns multiple results containing titles,
    snippets, and other relevant information from web pages.

    Args:
        query (str): The search query string to be executed.
                    Should be specific and well-formed for best results.
                    Example: "latest Python programming best practices 2024"

    Returns:
        list[dict]: A list of dictionaries containing search results.
        Each dictionary contains:
            - title (str): The title of the search result
            - snippet (str): A brief excerpt or description of the content
            - source (str): The source website or domain
            - date (str, optional): Publication date if available

    Notes:
        - The tool returns up to 10 search results per query
        - Results are sorted by relevance
        - Handles various types of queries including:
            * General information searches
            * Technical documentation lookups
            * Current events and news
            * Product information
        - Automatically handles URL encoding and special characters

    Limitations:
        - Requires valid API credentials
        - Subject to Google API rate limits and quotas
        - May not access paywalled or restricted content
        - Results may vary based on region and time

    Error Handling:
        - Returns empty list if no results found
        - Returns error information in case of API failures
        - Handles network timeouts and connection issues gracefully
    """
    try:
        import time
        time.sleep(2)
        data_from_search = google_search_var.run(query=query)
        print(data_from_search)
        return data_from_search
    except Exception as e:

        e_ = [{"error": f"Search failed: {str(e)}"}]
        print(e_)
        return json.dumps(e_)


search = google_search("Java Agentic AI jobs")
print(search)
#
# # Step 2: Create a Tool object for Google Search
# google_search_tool = Tool(
#     name="Google Search",
#     func=google_search.run,
#     description="A tool to perform Google searches. Use this to find current information or answers from the web."
# )
