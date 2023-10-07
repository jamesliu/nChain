import json
import numpy as np
import sqlite_utils
from sqlite_utils.db import Table
from typing import cast, List, Tuple, Optional, Union, Dict, Any
from .base_vectordb import VectorDatabase
from nchain.models.core import Entry
from annoy import AnnoyIndex
import struct
import time
import os

def encode(values):
    return struct.pack("<" + "f" * len(values), *values)

def encode_as_numpy(values):
    return np.array(values, dtype=np.float32).tobytes()

def decode(binary):
    return struct.unpack("<" + "f" * (len(binary) // 4), binary)

def decode_from_numpy_to_list(binary):
    numpy_array = np.frombuffer(binary, dtype=np.float32)
    return numpy_array.tolist()

class SQLiteVectorDB(VectorDatabase):

    def __init__(self, dimension: int, indexdb_path: str, db_path=None, metric: str = "angular", collection:str="default"):
        self.dimension = dimension
        self.indexdb_path = indexdb_path
        if db_path:
            self.db = sqlite_utils.Database(db_path)
        else:
            self.db = sqlite_utils.Database(memory=True)
        # Create the 'collections' table
        self.db["collections"].create({
            "id": int,     # unique identifier for each collection
            "name": str,   # name of the collection
            "model": str,   # identifier (or model ID) for the embedding model associated with the collection
            "dimension": int,
            "metric": str,
            "indexed_at":int, 
            "stored_at": int,
        }, pk="id", not_null=["name", "model"], if_not_exists=True)
        self.db["collections"].create_index(["name"], unique=True, if_not_exists=True)

        # Create the 'embeddings' table
        self.db["embeddings"].create({
            "collection_id": int,     # foreign key to reference the 'collections' table
            "id": int,                # identifier for the entry
            "embedding": "BLOB",      # embedded vector
            "content": str,           # content in text format
            "content_blob": "BLOB",   # content in binary format
            "content_hash": "BLOB",   # hash of the content for deduplication
            "metadata": str,          # additional metadata
            "updated": int            # timestamp
        }, pk=("id"), foreign_keys=[("collection_id", "collections", "id")], not_null=["collection_id", "id"], if_not_exists=True)  
        rows = list(self.db["collections"].rows_where("name = ?", [collection]))
        if len(rows) > 0:
            self.collection = rows[0]
            self.collection["metric"] = metric
            self.db["collections"].update(self.collection["id"], {"metric":metric} )
        else:
            collection_row = {
                "name": collection,
                "model": "SentenceTransformers",
                "dimension": dimension,
                "metric": metric,
                "indexed_at": None,
                "stored_at": None
            }
            self.db["collections"].insert(collection_row, replace=True)
            self.collection = list(self.db["collections"].rows_where("name = ?", [collection]))[0]
        if  os.path.exists(indexdb_path):
            self.index = AnnoyIndex(self.dimension, self.collection["metric"])
            self.index.load(indexdb_path)  # Load the Annoy index from disk
            self.vectors_updated = False
        else:
            self.vectors_updated = True

    def store_vectors(self, vectors: List[List[float]], metadata_list: List[dict], chunks: list[Union[str, bytes]], store:bool) -> None:
        hashes = [self.content_hash(content) for content in chunks]
        # Create a mapping of hash to its index for quick look-up
        hash_to_index = {hash: index for index, hash in enumerate(hashes)}
        
        # Fetch rows that match the provided hashes
        matching_rows = self.db.query(
            """
            select id, content_hash from embeddings
            where collection_id = ? and content_hash in ({})
            """.format(",".join("?" for _ in hashes)),
            [self.collection["id"]] + hashes
        )
        
        # Get the hash_index for each matching row
        existing_ids = [hash_to_index[row['content_hash']] for row in matching_rows]
        filtered_items = [item + (hashes[idx], ) for idx, item in enumerate(zip(vectors, metadata_list, chunks)) if idx not in existing_ids]
        if len(filtered_items) > 0:
            with self.db.conn:
                cast(Table, self.db["embeddings"]).insert_all(
                    (
                        {
                            "collection_id": self.collection["id"],
                            "embedding": encode_as_numpy(embedding),
                            "content": content 
                            if (store and isinstance(content, str))
                            else None,
                            "content_blob": content 
                            if (store and isinstance(content, bytes))
                            else None,
                            "content_hash": content_hash,
                            "metadata": json.dumps(metadata) if metadata else None,
                            "updated": int(time.time()),
                        }
                        for (embedding, metadata, content, content_hash) in filtered_items
                       
                    ),
                    replace=True,
                )
            
            self.collection["stored_at"] = int(time.time())
            self.db["collections"].update(self.collection["id"], {"stored_at":self.collection["stored_at"]})
            self.vectors_updated = True

    def build_index(self):
        self.index = AnnoyIndex(self.dimension, self.collection["metric"])
        for row in self.db["embeddings"].rows_where():
            numpy_array = np.frombuffer(row["embedding"], dtype=np.float32)
            self.index.add_item(row["id"], numpy_array.tolist())
        self.index.build(10)
        self.collection["indexed_at"] = int(time.time())
        self.db["collections"].update(self.collection["id"], {"indexed_at":self.collection["indexed_at"]})
        print("Index built", self.indexdb_path)
        self.index.save(self.indexdb_path)

    def refresh_index(self):
        if self.collection["stored_at"]:
            if self.collection["indexed_at"] is None or self.collection["stored_at"] > self.collection["indexed_at"]:
                self.build_index()
               
        self.vectors_updated = False
        
    def search_vectors(self, query_vector: List[float], top_k: int) -> List[Entry]:
        if self.vectors_updated:
            self.refresh_index()

        indices, distances = self.index.get_nns_by_vector(query_vector, top_k, include_distances=True)
        results = []
        for idx, distance in zip(indices, distances):
            row = self.db["embeddings"].get(idx)
            metadata = json.loads(row["metadata"])
            similar_entry = Entry(id=row["id"], score=distance, content=row["content"], metadata=metadata)
            results.append(similar_entry)
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

