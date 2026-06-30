import json

class JSONSerializableMixin:
    """Provides uniform JSON conversion."""
    def to_json(self):
        return json.dumps(self.__dict__, default=str)