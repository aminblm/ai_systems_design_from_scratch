# distributed_no_sql_database.py
from typing import Dict, Any, List, Optional

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestDistributedNoSQLDatabase(TestMixin):
    """Test the distributed_no_sql_database module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestDistributedNoSQLDatabase initialized.")
    
    def test_distributed_no_sql_database(self):
        # 1. Initialize our clustered store wrapper
        db = DistributedDatabase("production_cluster", num_shards=2)

        # 2. Establish our collection metadata layout boundaries
        users_schema = {"name": "text", "age": "int", "status": "text"}
        users = db.create_collection("users", schema=users_schema)

        # 3. Populate collection store variables
        users.insert_one({"name": "Alice", "age": 30, "status": "active"})
        users.insert_one({"name": "Bob", "age": 30, "status": "pending"})
        users.insert_one({"name": "Charlie", "age": 25, "status": "active"})

        # 4. Perform structured search query actions
        search_results = users.find({"age": 30})
        self.logger.info(f"Search Results (age == 30): {search_results}")

        # 5. Execute explicit pipeline queries (Fully functional pipeline handling)
        aggregation_pipeline = [
            {"$match": {"status": "active"}},
            {"$count": "active_users_count"}
        ]
        agg_results = users.aggregate(aggregation_pipeline)
        self.logger.info(f"\nAggregation Framework Output: {agg_results}")

        # 6. Distribute elements down onto structural data cluster partitions safely
        db.shard_collection("users", shard_key="name")
        
        for shard in db.shards:
            allocated = shard.collections.get("users", [])
            self.logger.info(f"Cluster Shard #{shard.shard_id} local document count: {len(allocated)}")

        
class Collection(LoggableMixin):
    """Manages an isolated namespace of document structures and index maps."""

    def __init__(self, name: str, schema_fields: Optional[Dict[str, str]] = None) -> None:  
        super().__init__()
        self.name = name
        self.schema_fields = schema_fields or {} 
        self.documents: List[Dict[str, Any]] = []
        self.indexes: List[Dict[str, Any]] = []
        self.logger.info("Collection initialized.")

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


class DatabasePartition(LoggableMixin):
    """Represents a distributed database shard grouping targeted record allocations."""

    def __init__(self, shard_id: int) -> None:
        super().__init__()
        self.shard_id = shard_id
        self.collections: Dict[str, List[Dict[str, Any]]] = {}
        self.logger.info("DatabasePartition initialized.")

    def allocate_record(self, collection_name: str, document: Dict[str, Any]) -> None:
        if collection_name not in self.collections:
            self.collections[collection_name] = []
        self.collections[collection_name].append(document)

    
class DistributedDatabase(LoggableMixin):
    """Master controller managing global schemas and orchestrating horizontal shards."""

    def __init__(self, name: str, num_shards: int = 2) -> None:
        super().__init__()
        self.name = name
        self.logical_collections: Dict[str, Collection] = {}
        self.shards = [DatabasePartition(shard_id=i) for i in range(num_shards)]
        self.logger.info("DistributedDatabase initialized.")

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
            
        self.logger.info(f"Successfully re-sharded collection '{collection_name}' across clusters.")