import requests
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_web(query, num_results=10):
    try:
        logger.info(f"Searching web for: {query}")
        url = "https://serpapi.com/search.json"
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": num_results,
            "safe": "active"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        organic_results = data.get("organic_results", [])
        urls = [result["link"] for result in organic_results if "link" in result]
        logger.info(f"Found {len(urls)} search results")
        return urls
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching web: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in search_web: {str(e)}")
        return []