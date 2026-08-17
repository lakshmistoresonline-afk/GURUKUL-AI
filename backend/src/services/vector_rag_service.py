import os
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import logging
from ..config.app_config import settings

logger = logging.getLogger(__name__)

class VectorRAGService:
    def __init__(self):
        self.persist_directory = os.path.join(settings.STORAGE_PATH, "vector_db")
        os.makedirs(self.persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="curriculum_knowledge",
            metadata={"hnsw:space": "cosine"}
        )

    async def add_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Add knowledge chunks to the vector database.
        Expected chunk format: {id, content, metadata}
        """
        ids = [c['id'] for r in chunks for c in ([r] if isinstance(r, dict) else [])] # Flatten if needed
        # Robust handling of input list
        ids = []
        documents = []
        metadatas = []

        for c in chunks:
            ids.append(str(c.get('id')))
            documents.append(c.get('content'))
            # Metadata must be simple dict with str, int, float, or bool
            meta = c.get('metadata', {})
            # Sanitize metadata for Chroma (ensure no nested dicts or None)
            sanitized_meta = {k: (v if v is not None else "") for k, v in meta.items() if isinstance(v, (str, int, float, bool))}
            metadatas.append(sanitized_meta)

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        logger.info(f"Added {len(ids)} chunks to Vector DB.")

    async def search(self, query: str, class_level: Optional[str] = None, subject: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search with curriculum filters.
        """
        where = {}
        if class_level:
            where["class_level"] = class_level
        if subject:
            where["subject"] = subject.lower()

        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where=where if where else None
        )

        output = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                output.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })

        return output

    async def delete_by_resource(self, resource_id: str):
        """Clean up all chunks associated with a resource."""
        self.collection.delete(where={"resource_id": resource_id})
        logger.info(f"Deleted chunks for resource: {resource_id}")

vector_rag = VectorRAGService()
