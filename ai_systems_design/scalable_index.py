import collections, logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class Shard:
    """An independent data partition inside an Index containing localized segment sheets."""

    def __init__(self, shard_id: int) -> None:
        self.shard_id = shard_id
        self.documents: List[Dict[str, Any]] = []

    def add_document(self, document: Dict[str, Any]) -> None:
        self.documents.append(document)


class ScalableIndex:
    """A resilient, schema-driven mock index utilizing linear data lookups and shard routing."""

    def __init__(self, name: str, mapping: Dict[str, Any], num_shards: int = 3) -> None:
        self.name = name
        self.mapping = mapping.get("properties", {})

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
                logger.warning(f"Unmapped field item dropped or ignored during ingestion: {field}")
        
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
            logger.error(f"Cannot perform text search operations on field type:'{search_field}'")

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