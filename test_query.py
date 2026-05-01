from services.processing_service import ProcessingService

processor = ProcessingService()

query = "What company the offer letter is from?"

result = processor.query(query)

print("\nAnswer:\n", result["answer"])
print("\nSources:\n", result["sources"])