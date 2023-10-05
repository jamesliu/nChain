import json
import numpy as np
import sqlite_utils
from typing import List, Tuple, Optional, Dict
from .base_vectordb import VectorDatabase
from annoy import AnnoyIndex

class SQLiteVectorDB(VectorDatabase):

    def __init__(self, dimension: int, db_path=None, metric: str = "euclidean"):
        self.dimension = dimension
        if db_path:
            self.db = sqlite_utils.Database(db_path)
        self.db = self.db or sqlite_utils.Database(memory=True)
        self.db["vectors"].create({
            "id": int,
            "vector": bytes,
            "metadata": str
        }, pk="id", if_not_exists=True)
        
        self.index = AnnoyIndex(dimension, metric)
        self.index_built = False

    def store_vectors(self, vectors: List[List[float]], metadata_list: List[dict]) -> None:
        for vector, meta in zip(vectors, metadata_list):
            numpy_array = np.array(vector, dtype=np.float32)
            blob = numpy_array.tobytes()
            metadata_string = json.dumps(meta)
            row = self.db["vectors"].insert({"vector": blob, "metadata": metadata_string})
            idx = row.last_pk
            self.index.add_item(idx, vector)
        self.vector_updated = True

    def refresh_index(self):
        # Drop the current index and create a new one
        self.index = AnnoyIndex(self.dimension, "euclidean")
        
        # Retrieve all vectors from the SQLite database and add them to the Annoy index
        for row in self.db["vectors"].rows_where():
            numpy_array = np.frombuffer(row["vector"], dtype=np.float32)
            self.index.add_item(row["id"], numpy_array.tolist())
        
        # Build the Annoy index
        self.index.build(10)
        self.vectors_updated = False
    

    def search_vectors(self, query_vector: List[float], top_k: int) -> List[Tuple[int, float, dict]]:
        if self.vector_updated:
            self.refresh_index()

        indices, distances = self.index.get_nns_by_vector(query_vector, top_k, include_distances=True)
        
        results = []
        for idx, distance in zip(indices, distances):
            row = self.db["vectors"].get(idx)
            metadata = json.loads(row["metadata"])
            results.append((idx, distance, metadata))
            
        return results

    def update_vector(self, index: int, new_vector: List[float], new_metadata: Optional[dict] = None) -> None:
        # Convert vector to BLOB
        numpy_array = np.array(new_vector, dtype=np.float32)
        blob = numpy_array.tobytes()
        # Update in SQLite
        self.db["vectors"].update(index, {"vector": blob, "metadata": json.dumps(new_metadata or {})})
        
        # Update in Annoy
        self.index.add_item(index, new_vector)
        self.index_built = False

    def delete_vector(self, index: int) -> None:
        self.db["vectors"].delete_where("id = ?", [index])
        self.vector_updated = True
        # Note: Deletion in Annoy isn't straightforward. One way is to rebuild the index excluding the deleted vector.
        # However, for simplicity, we're not handling it here. The deleted vector may still appear in search results.

