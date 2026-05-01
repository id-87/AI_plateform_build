import streamlit as st
from services.processing_service import ProcessingService

st.set_page_config(page_title="Drive RAG Assistant", layout="wide")

st.title("📂 Google Drive RAG Assistant")

# Initialize once
@st.cache_resource
def load_processor():
    return ProcessingService()

processor = load_processor()

# Input
query = st.text_input("Ask something about your documents:")

if st.button("Ask") and query:
    with st.spinner("Thinking..."):
        result = processor.query(query)

    st.subheader("Answer")
    st.write(result["answer"])

    if result["sources"]:
        st.subheader("Sources")
        for src in result["sources"]:
            st.write(f"- {src}")