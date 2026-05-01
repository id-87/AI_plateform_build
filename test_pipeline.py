# test_pipeline.py

import os
from dotenv import load_dotenv
from services.drive_service import DriveService
from services.embedding_service import EmbeddingService

load_dotenv()

FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

drive = DriveService()
embedder = EmbeddingService()

files = drive.list_files(FOLDER_ID)

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
    files = drive.list_files(FOLDER_ID)


    print(f"Chunks: {len(chunks)} | Embeddings: {len(embeddings)}")
print("FOLDER_ID:", FOLDER_ID)
print("Files fetched:", files)
print("Total files:", len(files))