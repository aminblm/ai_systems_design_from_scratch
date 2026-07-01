# json_serializable_mixin.py

"""Provides uniform JSON conversion."""

import json
from typing import Any

from ai_system_design.kernel.mixins import LoggableMixin


class JSONSerializableMixin(LoggableMixin):
    """Provides uniform JSON conversion."""

    def __init__(self) -> None:
        """JSONSerializableMixin Constructor."""
        super().__init__()
        self.logger.info("JSONSerializableMixin initialized.")

    def to_json(self, indent: int = 2):
        """JSONSerializableMixin Method."""
        return json.dumps(self.__dict__, default=str, indent=indent)
    
    def dumps(self, object: Any, indent: int = 2):
        """JSONSerializableMixin Method."""
        return json.dumps(object, default=str, indent=indent)
    
    def loads(self, s: str):
        """JSONSerializableMixin Method."""
        return json.loads(s)
    
    def load(self, f):
        """JSONSerializableMixin Method."""
        return json.load(f)

    def dump(self, obj: Any, f):
        """JSONSerializableMixin Method."""
        json.dump(obj, f)
    
    def get_JSONDecodeError(self):
        """JSONSerializableMixin Method."""
        return json.JSONDecodeError