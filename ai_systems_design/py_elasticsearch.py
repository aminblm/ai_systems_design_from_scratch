class Index:
    def __init__(self, name, mapping):
        self.name = name
        self.mapping = mapping 
        self.documents = []
        self.shards = []

    def add_document(self, document):
        self.documents.append(document)

    def search(self, query):
        results = []
        if query.get("term"):
            if "author" in self.mapping["properties"]:
                if self.mapping["properties"]["author"]["type"] == "text":
                    if query["term"]["author"] == "John Doe":
                        results = [doc for doc in self.documents if doc["author"] == "John Doe"]
        return results
    
    def aggregate(self, aggregation):
        if aggregation.get("term"):
            if "author" in self.mapping["properties"]:
                if self.mapping["properties"]["author"]["type"] == "text":
                    # Simple aggregation count documents per author
                    return {author: len([doc for doc in self.documents if doc["author"] == author]) for author in set(doc["author"] for doc in self.documents)}
                
    def allocate_shards(self, num_shards):
        self.shards = [self.documents[i % len(self.documents)] for i in range(num_shards)]

if __name__ == '__main__':
    index = Index("sample_index", {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "date": {"type": "date"}
        }
    })

    index.add_document({
        "title": "Sample Document",
        "author": "John Doe",
        "date": "2023-04-01"
    })

    index.add_document({
        "title": "Sample Document",
        "author": "John Pie",
        "date": "2023-04-01"
    })

    query = {
        "term": {"author": "John Doe"}
    }

    results = index.search(query)
    print("Search Results:", results)

    aggregation = {
        "term": {"field": "author"}
    }

    results = index.aggregate(aggregation)
    print("Aggregation Results:", results)

    index.allocate_shards(20)
    print("Shard Allocation:", index.shards)
