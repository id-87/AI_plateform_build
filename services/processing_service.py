# services/processing_service.py

from services.embedding_service import EmbeddingService
from services.pinecone_service import PineconeService
from services.llm_service import LLMService


class ProcessingService:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.pinecone = PineconeService()
        self.llm = LLMService()

    def _build_context(self, matches):
        context_chunks = []
        sources = set()

        for match in matches:
            metadata = match.get("metadata", {})
            text = metadata.get("text", "")
            source = metadata.get("source", "unknown")

            if text:
                context_chunks.append(text)
                sources.add(source)

        context = "\n\n".join(context_chunks)
        return context, list(sources)

    def query(self, user_query):
        # 1. Embed query
        query_embedding = self.embedder.embed_texts([user_query])[0]

        # 2. Search Pinecone
        matches = self.pinecone.query(query_embedding, top_k=5)

        if not matches:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        # 3. Build context
        context, sources = self._build_context(matches)

        # 4. Call LLM
        answer = self.llm.generate(user_query, context)

        return {
            "answer": answer,
            "sources": sources
        }