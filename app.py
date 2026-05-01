import streamlit as st
from services.processing_service import ProcessingService
from services.ingest_service import IngestService

st.set_page_config(page_title="Drive RAG Assistant", layout="wide")

st.title("📂 Google Drive RAG Assistant")

# Load services once
@st.cache_resource
def load_services():
    return ProcessingService(), IngestService()

processor, ingestor = load_services()

# =========================
# 🔄 SYNC BUTTON
# =========================
st.subheader("Sync Data")

if st.button("🔄 Sync Drive"):
    with st.spinner("Syncing Drive and updating embeddings..."):
        result = ingestor.ingest()

    st.success("✅ Sync completed")

    # 🔍 DEBUG OUTPUT
    st.subheader("Debug Info")
    st.json(result)


if st.button("📊 Check Pinecone"):
    stats = ingestor.pinecone.index.describe_index_stats()
    st.json(stats)
# =========================
# 💬 QUERY
# =========================
st.subheader("Ask Questions")

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