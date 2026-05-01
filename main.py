from fastapi import FastAPI
from services.processing_service import ProcessingService

app = FastAPI()
processor = ProcessingService()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/ask")
def ask(query: str):
    result = processor.query(query)
    return result