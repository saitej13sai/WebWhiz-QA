# 🌐 WebWhiz QA

**WebWhiz QA** is an intelligent web-based Q&A system that lets users ask natural language questions and receive real-time answers with source links. It leverages FastAPI for the backend, Google Gemini for language generation, SerpAPI for web search, and newspaper3k + BeautifulSoup for article scraping. Includes both a static HTML frontend and a Streamlit interface.

---

## 🚀 Features

- 🔍 Web search with [SerpAPI](https://serpapi.com/)
- 🧠 LLM-based answers using [Gemini Pro](https://ai.google.dev/)
- 📄 Article parsing using `newspaper3k` & `BeautifulSoup`
- 💬 FastAPI backend with CORS enabled
- 🖥️ Frontend options: Streamlit app or HTML UI
- 🔗 Reliable sources returned with each answer

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Requests, newspaper3k, BeautifulSoup
- **LLM:** Google Gemini API
- **Search:** SerpAPI
- **Frontend:** Streamlit / HTML + JS
- **Runtime:** Python 3.10+

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/saitej13sai/WebWhiz-QA.git
cd WebWhiz-QA
