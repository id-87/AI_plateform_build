# embedding_service.py

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None  # lazy load

    def load_model(self):
        if self.model is None:
            print("🔄 Loading embedding model...")
            self.model = SentenceTransformer(self.model_name)

    def chunk_text(self, text, chunk_size=500, overlap=100):
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i+chunk_size])
        return chunks

    def embed_texts(self, texts):
        self.load_model()
        return self.model.encode(texts).tolist()