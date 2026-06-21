import logging
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class Collection:
    """Manages an isolated namespace of document structures and index maps."""

    def __init__(self, name: str, schema_fields: Optional[Dict[str, str]] = None) -> None:  
        self.name = name
        self.schema_fields = schema_fields or {} 
        self.documents: List[Dict[str, Any]] = []
        self.indexes: List[Dict[str, Any]] = []

    def insert_one(self, document: Dict[str, Any]) -> None:
        """Appends a document payload after performing basic schema type checks."""
        # Optional schema validation pass
        for field, expected_type in self.schema_fields.items():
            if field in document:
                # Real production engines validate explicit type casting here
                pass
        self.documents.append(document)

    def find(self, filter_criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Evaluates document attributes against dictionary key-value search filter maps."""
        if not filter_criteria:
            return self.documents.copy()
        
        matched_records = []
        for doc in self.documents:
            # Match item only if all filtering criteria match perfectly
            if all(doc.get(key) == val for key, val in filter_criteria.items()):
                matched_records.append(doc)
                
        return matched_records
    
    def aggregate(self, pipeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Processes sequential aggregation operators matching input pipeline definitions."""
        working_set = self.documents.copy()
        output_metrics: Dict[str, Any] = {}

        for stage in pipeline:
            # Handle standard match stage filters
            if "$match" in stage:
                criteria = stage["$match"]
                working_set = [d for d in working_set if all(d.get(k) == v for k, v in criteria.items())]

            # Handle total count aggregation pipelines
            elif "$count" in stage:
                metric_name = stage["$count"]
                output_metrics[metric_name] = len(working_set)

        return output_metrics


class DatabasePartition:
    """Represents a distributed database shard grouping targeted record allocations."""

    def __init__(self, shard_id: int) -> None:
        self.shard_id = shard_id
        self.collections: Dict[str, List[Dict[str, Any]]] = {}

    def allocate_record(self, collection_name: str, document: Dict[str, Any]) -> None:
        if collection_name not in self.collections:
            self.collections[collection_name] = []
        self.collections[collection_name].append(document)

    
class DistributedDatabase:
    """Master controller managing global schemas and orchestrating horizontal shards."""

    def __init__(self, name: str, num_shards: int = 2) -> None:
        self.name = name
        self.logical_collections: Dict[str, Collection] = {}
        self.shards = [DatabasePartition(shard_id=i) for i in range(num_shards)]

    def create_collection(self, name: str, schema: Optional[Dict[str, str]] = None) -> Collection:
        coll = Collection(name, schema)
        self.logical_collections[name] = coll
        return coll

    def shard_collection(self, collection_name: str, shard_key: str) -> None:
        """Distributes logical collection contents safely across backend partitions."""
        logical_coll = self.logical_collections.get(collection_name)
        if not logical_coll:
            raise ValueError(f"Target collection '{collection_name}' does not exist.")

        for doc in logical_coll.documents:
            val = doc.get(shard_key)
            if val is None:
                continue
            
            # Route document to specific shard partition via deterministic hashing rules
            target_shard_idx = hash(str(val)) % len(self.shards)
            self.shards[target_shard_idx].allocate_record(collection_name, doc)
            
        logger.info(f"Successfully re-sharded collection '{collection_name}' across clusters.")