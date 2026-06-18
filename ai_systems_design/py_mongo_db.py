class Database:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, name):
        self.name = name
        self.collections = []


class Collection:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, name, fields=None):
        self.name = name
        self.fields = fields or {} 
        self.documents = []
        self.indexes = []

    def insert(self, document):
        self.documents.append(document)

    def find(self, filter=None):
        return [doc for doc in self.documents if filter]
    
    def aggregate(self, pipeline):
        # Simple aggregate
        return {field: len([doc for doc in self.documents if doc[field]]) for field in self.fields}
    
    def create_index(self, index):
        self.indexes.append(index)

    def shard(self, num_shards):
        self.shards = [self.documents[i % len(self.documents)] for i in range(num_shards)]


class Document:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, data):
        self.data = data

    
class Index:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


class Query:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, filter=None, sort=None, limit=None):
        self.filter = filter
        self.sort = sort 
        self.limit = limit

    
class Aggregation:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, pipeline):
        self.pipeline = pipeline


class Sharding:
    def __init__(self, database):
        self.database = database
        self.shards = []


if __name__ == "__main__":
    db = Database("mydb")

    collection = Collection("users", {"name": "text", "age": "int"})

    collection.insert({"name": "Alice", "age": "30"})

    results = collection.find({"age":"30"})
    print(results)

    aggregation = Aggregation([
        {"$count": "age"}
    ])
    results = collection.aggregate(aggregation)
    print(results)

    collection.shard(2)
    print(collection.shards)