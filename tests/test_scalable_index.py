from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.scalable_index import ScalableIndex


class TestScalableIndex(TestMixin):
    """Test the scalable_index module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestScalableIndex initialized.")

    def test(self):
        super().test()
        # Initialise index schema configuration boundaries safely
        schema_config = {
            "properties": {
                "title": {"type": "text"},
                "author": {"type": "text"},
                "date": {"type": "date"}
            }
        }

        # Spin up an index containing 4 dinstinct shards
        search_index = ScalableIndex("production_index", schema_config, num_shards=4)

        # Ingest data targets passing distinct system ID routing handles
        search_index.add_document(document_id=101, document={
            "title": "Design Patterns", "author": "John Doe", "date": "2026-01-01"
        })
        search_index.add_document(document_id=102, document={
            "title": "Concurrent Computing", "author": "John Pie", "date": "2026-03-15"
        })
        search_index.add_document(document_id=103, document={
            "title": "Distributed Systems Handbook", "author": "John Doe", "date": "2026-05-20"
        })

        # Execute dynamic search query
        pie_query = {"term": {"author": "John Pie"}}
        doe_query = {"term": {"author": "John Doe"}}

        self.logger.info(f"Search Results (John Pie): {search_index.search(pie_query)}")
        self.logger.info(f"Search Results (John Doe): {search_index.search(doe_query)}")

        # Evalue aggregations
        author_aggregation = {"term": {"field": "author"}}
        self.logger.info(f"Aggregation Results (Author): {search_index.aggregate_counts(author_aggregation)}")

        # Self.logger.info out actual distributed allocation struction across partitions
        for shard in search_index.shards:
            self.logger.info(f"Shard {shard.shard_id} allocation storage list size: {len(shard.documents)}") 