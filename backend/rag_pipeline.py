import os
import requests
from scrape import scrape_urls
from search import search_web
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def answer_question(query):
    try:
        logger.info(f"Starting search for query: {query}")
        urls = search_web(query)
        logger.info(f"Found {len(urls)} URLs")
        
        if not urls:
            return {
                "answer": "I couldn't find any relevant sources for your question. Please try rephrasing your query.",
                "sources": []
            }
        
        texts = scrape_urls(urls)
        logger.info(f"Scraped {len(texts)} articles")
        
        context = "\n\n".join(texts[:3])
        prompt = f"""
        Based on the following web sources, provide a comprehensive and accurate answer to the question...
        Context from web sources:
        {context}
        Question: {query}
        Please provide a detailed answer that:
        1. Directly addresses the question
        2. Uses information from the provided sources
        3. Is well-formatted and easy to read
        4. Includes specific details and examples when relevant
        Answer:
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            logger.error(f"Gemini API error: {response.status_code} - {response.text}")
            return {
                "answer": "I'm having trouble generating an answer right now. Please try again later.",
                "sources": urls
            }
        
        result = response.json()
        answer = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No answer found.")
        
        return {
            "answer": answer,
            "sources": urls[:5]
        }
        
    except Exception as e:
        logger.error(f"Error in answer_question: {str(e)}")
        return {
            "answer": f"I encountered an error while processing your question: {str(e)}",
            "sources": []
        }