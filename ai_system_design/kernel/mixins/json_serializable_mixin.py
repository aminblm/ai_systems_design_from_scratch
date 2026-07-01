import json

from ai_system_design.kernel.mixins import LoggableMixin


class JSONSerializableMixin(LoggableMixin):
    """Provides uniform JSON conversion."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("JSONSerializableMixin initialized.")

    def to_json(self):
        return json.dumps(self.__dict__, default=str)