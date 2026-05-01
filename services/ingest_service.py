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
        debug = {
            "files_found": 0,
            "files_processed": 0,
            "chunks_uploaded": 0,
            "errors": []
        }

        files = self.drive.list_files(self.folder_id)
        debug["files_found"] = len(files)

        for file in files:
            try:
                if file["mimeType"] not in ["application/pdf", "text/plain"]:
                    continue

                debug["files_processed"] += 1

                stream = self.drive.download_file(file["id"])
                text = self.drive.extract_text(stream, file["mimeType"])

                if not text:
                    debug["errors"].append(f"No text: {file['name']}")
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

                debug["chunks_uploaded"] += len(vectors)

            except Exception as e:
                debug["errors"].append(f"{file['name']} → {str(e)}")

        return debug
