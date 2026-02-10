from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings


class MindTraceVectorStore:
    """
    Chroma-backed vector store for MindTrace.
    Responsible ONLY for storage and retrieval of session embeddings.
    """

    def __init__(self, persist_dir: str = "data/chroma"):
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_dir,
                is_persistent=True, 
                anonymized_telemetry=False,
            )
        )

    def _collection_name(self, user_id: str) -> str:
        return f"mindtrace_user_{user_id}"

    def get_or_create_collection(self, user_id: str):
        return self.client.get_or_create_collection(
            name=self._collection_name(user_id)
        )

    # -------- Write --------

    def upsert_session(
        self,
        user_id: str,
        session_id: str,
        embedding: List[float],
        text: str,
        metadata: Dict,
    ):
        collection = self.get_or_create_collection(user_id)

        collection.upsert(
            ids=[session_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
        )

        

    # -------- Read --------

    def query_similar_sessions(
        self,
        user_id: str,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None,
    ) -> List[str]:
        """
        Returns session_ids of semantically similar sessions.
        Does NOT return insights or interpretations.
        """
        collection = self.get_or_create_collection(user_id)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        return results.get("ids", [[]])[0]

    # -------- Delete --------

    def delete_session(self, user_id: str, session_id: str):
        collection = self.get_or_create_collection(user_id)
        collection.delete(ids=[session_id])

    def delete_user(self, user_id: str):
        self.client.delete_collection(self._collection_name(user_id))
