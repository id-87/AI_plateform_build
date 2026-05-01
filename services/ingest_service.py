# services/ingest_service.py

from services.drive_service import DriveService
from services.embedding_service import EmbeddingService
from services.pinecone_service import PineconeService
import os
from dotenv import load_dotenv

load_dotenv()


class IngestService:
    def __init__(self):
        self.drive = DriveService()
        self.embedder = EmbeddingService()
        self.pinecone = PineconeService()
        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

    def ingest(self):
        files = self.drive.list_files(self.folder_id)

        total_files = 0
        total_chunks = 0

        for file in files:
            if file["mimeType"] not in ["application/pdf", "text/plain"]:
                continue

            total_files += 1
            print(f"Processing: {file['name']}")

            stream = self.drive.download_file(file["id"])
            text = self.drive.extract_text(stream, file["mimeType"])

            if not text:
                continue

            chunks = self.embedder.chunk_text(text)
            embeddings = self.embedder.embed_texts(chunks)

            vectors = [
                {
                    "id": f"{file['id']}_{i}",
                    "values": embeddings[i],
                    "metadata": {
                        "text": chunks[i],
                        "source": file["name"]
                    }
                }
                for i in range(len(chunks))
            ]

            self.pinecone.upsert(vectors)

            total_chunks += len(vectors)

        return {
            "files_processed": total_files,
            "chunks_uploaded": total_chunks
        }