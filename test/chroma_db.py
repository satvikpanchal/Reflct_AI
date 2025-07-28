import chromadb

client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection("memory")

collection.add(documents=["Satvik's age is 1000"], ids=["2"])
results = collection.query(query_texts=["Satvik's age"], n_results=1)
print(results)
