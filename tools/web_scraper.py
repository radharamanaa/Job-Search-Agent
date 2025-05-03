import requests
from bs4 import BeautifulSoup
import trafilatura
from typing import Optional
import logging
from urllib.parse import urlparse
logging.basicConfig(level=logging.INFO)
import json
logger = logging.getLogger(__name__)
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
def __validate_url(url: str) -> bool:
    """Validate if the URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        logger.error(f"Invalid URL format: {e}")
        return False

def __fetch_page(url: str) -> Optional[str]:
    """Fetch the webpage content."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching page: {e}")
        return None

def __extract_with_trafilatura(html_content: str) -> Optional[str]:
    """Extract content using trafilatura library."""
    try:
        extracted_text = trafilatura.extract(html_content)
        return extracted_text
    except Exception as e:
        logger.error(f"Trafilatura extraction failed: {e}")
        return None

def __extract_with_beautifulsoup(html_content: str) -> Optional[str]:
    """Extract content using BeautifulSoup as fallback."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
    
        # Remove unwanted elements
        for element in soup(['script', 'style', 'header', 'footer', 'nav']):
            element.decompose()
    
        # Get text content
        text = soup.body.get_text(separator='\n', strip=True) if soup.body else None
        return text
    except Exception as e:
        logger.error(f"BeautifulSoup extraction failed: {e}")
        return None

def extract_content(url: str) -> str:
    """
    Extracts and processes HTML content from a given URL, removing unnecessary elements
    and returning clean text content in a structured format.

    This function performs the following operations:
    1. Validates the input URL format
    2. Fetches the webpage content
    3. Processes the HTML to remove unwanted elements (scripts, styles, headers, etc.)
    4. Extracts clean text content

    Args:
        url (str): The complete URL of the webpage to scrape (e.g., 'https://example.com')

    Returns:
        str: A JSON string containing:
            - status: 'success' or 'error'
            - content: Extracted text content if successful, None if failed
            - error: Error message if failed, None if successful

    Example:
        >>> result = extract_content('https://example.com')
        >>> parsed_result = json.loads(result)
        >>> if parsed_result['status'] == 'success':
        ...     print(parsed_result['content'])
        ... else:
        ...     print(f"Error: {parsed_result['error']}")

    Notes:
        - The function removes common non-content elements like scripts, styles,
          headers, footers, and navigation bars
        - Returns structured JSON string for consistent error handling and processing
        - URL validation ensures the input follows proper URL format
        - Content extraction uses BeautifulSoup for reliable HTML parsing

    Raises:
        No exceptions are raised; all errors are handled and returned in the response
    """
    logger.info(f"URL to scrape: {url}")
    import time
    time.sleep(2)
    if not __validate_url(url):
        return json.dumps({
            'status': 'error',
            'content': None,
            'error': 'Invalid URL format'
        })

    html_content = __fetch_page(url)
    if not html_content:
        return json.dumps({
            'status': 'error',
            'content': None,
            'error': 'Failed to fetch page'
        })

# Try trafilatura first
    content = __extract_with_trafilatura(html_content)

# Fall back to BeautifulSoup if trafilatura fails
    if not content:
        content = __extract_with_beautifulsoup(html_content)
    
    if not content:
        return json.dumps({
            'status': 'error',
            'content': None,
            'error': 'Failed to extract content'
        })
    
    return json.dumps({
        'status': 'success',
        'content': content,
        'error': None
    })


