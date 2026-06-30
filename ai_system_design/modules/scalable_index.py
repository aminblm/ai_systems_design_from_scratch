# scalable_index.py
import collections
from typing import Dict, Any, List

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


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

        
class Shard(LoggableMixin):
    """An independent data partition inside an Index containing localized segment sheets."""

    def __init__(self, shard_id: int) -> None:
        super().__init__()
        self.shard_id = shard_id
        self.documents: List[Dict[str, Any]] = []
        self.logger.info("Shard initialized.")

    def add_document(self, document: Dict[str, Any]) -> None:
        self.documents.append(document)


class ScalableIndex(LoggableMixin):
    """A resilient, schema-driven mock index utilizing linear data lookups and shard routing."""

    def __init__(self, name: str, mapping: Dict[str, Any], num_shards: int = 3) -> None:
        super().__init__()
        self.name = name
        self.mapping = mapping.get("properties", {})
        self.logger.info("ScalableIndex initialized.")

        # Instanciate structural underlying shards correctly
        self.shards = [Shard(shard_id=i) for i in range(num_shards)]

    def _get_shard_route(self, document_id: int) -> Shard:
        """Determines consistent deterministic shard placement using simple hashing"""
        # Standard hash routing algoriths: Shard = hash(routing_key) % total_shards
        return self.shards[document_id % len(self.shards)]

    def add_document(self, document_id: int, document: Dict[str, Any]) -> None:
        """Validates incoming properties against active fields and routes to its shards."""
        # Schema field validation
        for field in document:
            if field not in self.mapping:
                self.logger.warning(f"Unmapped field item dropped or ignored during ingestion: {field}")
        
        target_shard = self._get_shard_route(document_id)
        target_shard.add_document(document)
        
    def _all_documents(self) -> List[Dict[str, Any]]:
        """Collects across distributed sub-partitions smoothly."""
        flat_list = []
        for shard in self.shards:
            for doc in shard.documents:
                flat_list.append(doc)
        return flat_list

    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Performs a dynamic, decoupled data pass across all document collections."""
        term_clause = query.get("term")
        if not term_clause:
            return []
        
        # Safely extract target field keys dynamically (e.g. 'author')
        search_field, target_value = next(iter(term_clause.items()))

        # Validate structural typing constraints
        if search_field not in self.mapping or self.mapping[search_field].get("type") != "text":
            self.logger.error(f"Cannot perform text search operations on field type:'{search_field}'")

        # Abstract lookup: $O(N)$ linear filter scan replacing hardcoded rules
        return [
            doc for doc in self._all_documents()
            if doc.get(search_field) == target_value
        ]
    
    def aggregate_counts(self, aggregation: Dict[str, Any]) -> Dict[str, int]:
        """Calculates item tallies safely in linear $O(N)$ runtime performance."""
        term_clause = aggregation.get("term")
        if not term_clause:
            return {}
        
        target_field = term_clause.get("field")
        if not target_field or target_field not in self.mapping:
            return {}
        
        # Optimized tracking using collection counter buckets
        counts = collections.Counter()
        for doc in self._all_documents():
            val = doc.get(target_field)
            if val is not None:
                counts[val] += 1

        return dict(counts)