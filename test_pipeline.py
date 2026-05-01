# test_pipeline.py

import os
from dotenv import load_dotenv
from services.drive_service import DriveService
from services.embedding_service import EmbeddingService
from services.pinecone_service import PineconeService

load_dotenv()

FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

drive = DriveService()
embedder = EmbeddingService()

files = drive.list_files(FOLDER_ID)
pinecone = PineconeService()

for file in files:
    if file["mimeType"] not in ["application/pdf", "text/plain"]:
        continue

    print(f"\nProcessing: {file['name']}")

    stream = drive.download_file(file["id"])
    text = drive.extract_text(stream, file["mimeType"])

    if not text:
        continue

    chunks = embedder.chunk_text(text)
    embeddings = embedder.embed_texts(chunks)

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

    pinecone.upsert(vectors)

    print(f"Chunks: {len(chunks)} | Uploaded: {len(vectors)}")