import faiss
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from .base_vectordb import VectorDatabase

class FaissVectorDB(VectorDatabase):

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.metadata = []

        # Use a flat index for simplicity
        self.index = faiss.IndexFlatL2(self.dimension)

    def store_vectors(self, vectors: List[List[float]], metadata: List[dict]) -> None:
        if not vectors:
            return

        # Convert input vectors to a numpy array
        faiss_vectors = np.array(vectors).astype('float32')

        # Add vectors to the index
        self.index.add(faiss_vectors)
    
        # Store metadata
        self.metadata.extend(metadata)

    def search_vectors(self, query_vector: List[float], top_k: int) -> List[Tuple[int, float, dict]]:
        # Convert query_vector to a numpy array
        query = np.array([query_vector]).astype('float32')
    
        # Search the index
        distances, indices = self.index.search(query, top_k)
    
        # Fetch metadata for the resulting indices
        results = [(int(idx), float(dist), self.metadata[int(idx)]) for idx, dist in zip(indices[0], distances[0])]
        return results

    def delete_vector(self, index: int) -> None:
        # In an in-memory Faiss index, we don't have a direct delete.
        # So, we reconstruct the index without the vector at the given index.
        vectors = self.index.reconstruct_n(0, self.index.ntotal)
        new_vectors = [v for i, v in enumerate(vectors) if i != index]
        new_metadata = [m for i, m in enumerate(self.metadata) if i != index]
        self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.store_vectors(new_vectors, new_metadata)

    def update_vector(self, index: int, new_vector: List[float], new_metadata: Optional[dict] = None) -> None:
        self.delete_vector(index)
        self.store_vectors([new_vector], [new_metadata or self.metadata[index]])
