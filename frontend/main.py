import streamlit as st
import requests

st.set_page_config(page_title="WebWhiz QA", layout="centered")

# ---- Styling ----
st.markdown("""
    <style>
        .main {
            background-color: #f4f4f4;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1rem;
            margin-bottom: 2rem;
        }
        .source-link {
            display: block;
            margin-top: 0.5rem;
            color: #4f46e5;
        }
        .answer-box {
            margin-top: 1.5rem;
            padding: 1rem;
            background: #f9fafb;
            border-left: 5px solid #667eea;
            border-radius: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown("<h1>🌐 WebWhiz QA</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask a question and get real-time answers from the web</div>', unsafe_allow_html=True)

# ---- Input ----
question = st.text_input("Enter your question here:")

if st.button("🔍 Get Smart Answer") and question:
    with st.spinner("⏳ Searching the web..."):
        try:
            response = requests.get("http://127.0.0.1:8000/ask", params={"q": question})
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("answer"):
                    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                    st.markdown(data["answer"].replace("\n", "<br>"), unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    if data.get("sources"):
                        st.markdown("#### Sources:")
                        for source in data["sources"]:
                            st.markdown(f'<a class="source-link" href="{source}" target="_blank">{source}</a>', unsafe_allow_html=True)
                    else:
                        st.info("No sources found.")
                else:
                    st.warning("No answer returned. Try rephrasing your question.")
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
