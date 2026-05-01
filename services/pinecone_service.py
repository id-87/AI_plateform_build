# services/pinecone_service.py

import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()


class PineconeService:
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX_NAME")

        if not api_key or not index_name:
            raise ValueError("Pinecone env variables missing")

        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)

    def upsert(self, vectors):
        """
        vectors = [
            {
                "id": "unique_id",
                "values": [embedding],
                "metadata": {"text": "...", "source": "..."}
            }
        ]
        """
        if not vectors:
            return

        self.index.upsert(
        vectors=vectors,
        namespace="default"
    )

    def query(self, embedding, top_k=5):
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            namespace="default"
        )

        return results.get("matches", [])