# test_distributed_no_sql_database.py
from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.distributed_no_sql_database import DistributedDatabase


class TestDistributedNoSQLDatabase(TestMixin):
    """Test the distributed_no_sql_database module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestDistributedNoSQLDatabase initialized.")
    
    def test(self):
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
