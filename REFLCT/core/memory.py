# import chromadb
# import google.generativeai as genai
# from config import CHROMA_DB_PATH

# class MemoryManager:
#     def __init__(self, persist_dir=CHROMA_DB_PATH):
#         self.client = chromadb.PersistentClient(path=persist_dir)
#         self.collection = self.client.get_or_create_collection(
#             name="agent_memory"
#         )

#     def _embed(self, text: str):
#         """Use Gemini free-tier embeddings"""
#         result = genai.embed_content(
#             model="models/text-embedding-004",
#             content=text,
#         )
#         return result["embedding"]

#     def add(self, content: str, metadata: dict = None):
#         self.collection.add(
#             documents=[content],
#             metadatas=[metadata or {}],
#             ids=[str(hash(content))],
#             embeddings=[self._embed(content)]
#         )

#     def query(self, query: str, n_results: int = 3):
#         return self.collection.query(
#             query_embeddings=[self._embed(query)],
#             n_results=n_results
#         )

from sentence_transformers import SentenceTransformer
import uuid
import chromadb

class MemoryManager:
    def __init__(self, persist_dir):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")  # small + fast
        self.collection = self.client.get_or_create_collection(name="agent_memory")

    def _embed(self, text: str):
        return self.embedder.encode(text).tolist()

    def add(self, content: str, metadata: dict = None, id: str = None):
        """
        Add a document to Chroma with embeddings and unique ID.
        """
        if id is None:
            id = str(uuid.uuid4())

        self.collection.add(
            documents=[content],
            metadatas=[metadata or {}],
            ids=[id],
            embeddings=[self._embed(content)]
        )

    def query(self, query: str, n_results: int = 3):
        return self.collection.query(
            query_embeddings=[self._embed(query)],
            n_results=n_results
        )
    
    def print_all(self):
        results = self.collection.get()
        print("\n📚 ALL MEMORY ENTRIES:")
        for i, doc in enumerate(results["documents"]):
            print(f"ID: {results['ids'][i]} | Doc: {doc} | Meta: {results['metadatas'][i]}")

