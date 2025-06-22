from newspaper import Article  # Correct import
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

def scrape_urls(urls, max_articles=5):
    texts = []
    processed = 0
    
    for url in urls:
        if processed >= max_articles:
            break
        try:
            logger.info(f"Scraping: {url}")
            article = Article(url)
            article.download()
            article.parse()
            
            if article.text and len(article.text.strip()) > 100:
                texts.append(f"Source: {url}\n{article.text[:2000]}...")
                processed += 1
                logger.info(f"Successfully scraped article from {url}")
            else:
                text = scrape_with_bs4(url)
                if text:
                    texts.append(f"Source: {url}\n{text}")
                    processed += 1
        except Exception as e:
            logger.warning(f"Failed to scrape {url}: {str(e)}")
            continue
    
    logger.info(f"Successfully scraped {len(texts)} articles")
    return texts

def scrape_with_bs4(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text[:2000] if len(text) > 2000 else text
    except Exception as e:
        logger.warning(f"BeautifulSoup scraping failed for {url}: {str(e)}")
        return None