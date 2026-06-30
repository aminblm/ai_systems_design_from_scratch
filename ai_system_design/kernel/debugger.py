# debugger.py
from typing import Any
from pprint import pprint
import pdb 

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestDebugger(TestMixin):
    """Test the debugger module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestDebugger initialized.")

    def test_debugger(self):
        debugger = Debugger()
        debugger.debug("debugger", debugger)
          

class Debugger(LoggableMixin):
    def __init__(self) -> None:
        super().__init__()
        self.logger.info("Debugger initialized.")

    def __repr__(self) -> str:
        return str(self.__dict__)

    def debug(self, arg_name: str, arg: Any) -> None:
        """Debug function used for debugging"""
        self.logger.debug(f"----------------------------DEBUGGING---------------------------")
        self.logger.debug("")
        pprint(f"{arg_name}={arg}")
        self.logger.debug("")
        self.logger.debug(f"----------------------------------------------------------------")
        pdb.set_trace()