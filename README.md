# 📂 Google Drive RAG Assistant

A simple Retrieval-Augmented Generation (RAG) system that:
- Fetches files from Google Drive
- Extracts and embeds content
- Stores embeddings in Pinecone
- Answers questions using Groq LLM

---

## 🚀 Features

- 📁 Google Drive integration (PDF, TXT)
- 🧠 Semantic search with Pinecone
- 🤖 LLM responses using Groq
- ⚡ FastAPI backend / Streamlit UI (optional)


---

## 🛠️ Setup

1. Clone the repo- https://github.com/id-87/AI_plateform_build

2. pip install -r requirements.txt

3. Configure a .env like :
    PINECONE_API_KEY=your_key
    PINECONE_INDEX_NAME=gdrive-rag
    GROQ_API_KEY=your_key
    GROQ_MODEL=llama-3.3-70b-versatile
    GOOGLE_DRIVE_FOLDER_ID=your_folder_id



### Hosted link usage instructions

1. Add the files in the given public drive link.
2. Go to the deployed URL and then you can directly interact with the system to talk to you documents.

Deployed URL- https://aiplateformbuild-icicnng9ahnanjim5hae8u.streamlit.app/
Drive Link- https://drive.google.com/drive/folders/1tu21LgmL17vIeRJtUlmE0-dPS627sQ4l

