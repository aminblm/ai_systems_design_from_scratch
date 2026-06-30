from typing import Any

from ai_system_design.kernel.loggable_mixin import LoggableMixin


class TestMixin(LoggableMixin):
    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestMixin initialized.")

    def __repr__(self) -> str:
        return str(self.__dict__)
