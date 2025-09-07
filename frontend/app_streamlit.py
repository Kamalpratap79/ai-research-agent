import streamlit as st
import requests

API_URL = "http://localhost:8000/research/research"  # matches backend

st.title("AI Agent")

query = st.text_input("Enter your research topic:")

num_results = st.slider("Number of results:", min_value=1, max_value=10, value=5)

summary_type = st.selectbox("Summary type:", ["bullet", "paragraph", "table"])

if st.button("Generate Summary") and query:
    with st.spinner("Fetching and summarizing..."):
        payload = {
            "query": query,
            "num_results": num_results,
            "summary_type": summary_type
        }
        try:
            response = requests.post(API_URL, json=payload, timeout=60)  # POST instead of GET
            response.raise_for_status()
            data = response.json()

            st.subheader("Summary")
            st.write(data.get("summary", "No summary found."))

            st.subheader("Sources")
            for s in data.get("sources", []):
                # Handle if backend returns list of strings or dicts
                if isinstance(s, str):
                    st.markdown(f"[{s}]({s})")
                else:
                    st.markdown(
                        f"[{s.get('title', 'No Title')}]({s.get('url', '#')}) - {s.get('date', 'Unknown')}"
                    )
        except Exception as e:
            st.error(f"Error: {e}")
