from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import answer_question
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WebWhiz QA API",
    description="Intelligent web search and question answering system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "WebWhiz QA API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/ask")
def ask_question(q: str = Query(..., description="Your question")):
    try:
        logger.info(f"Received question: {q}")
        result = answer_question(q)
        logger.info(f"Generated answer for question: {q}")
        return {
            "question": q,
            "answer": result["answer"],
            "sources": result["sources"],
            "success": True
        }
    except Exception as e:
        logger.error(f"Error processing question '{q}': {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}