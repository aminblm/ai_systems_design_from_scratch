from typing import Any
from pprint import pprint
import pdb 

from ai_system_design.kernel.loggable_mixin import LoggableMixin

def test_debugger():
    debugger = Debugger()
    debugger.debug("debugger", debugger)

class Debugger(LoggableMixin):
    def __init__(self):
        super().__init__()
        self.logger.info("Debugger initialized.")

    def debug(self, arg_name: str, arg: Any) -> None:
        self.logger.debug(f"----------------------------DEBUGGING---------------------------")
        pprint(f"{arg_name}={arg}")
        self.logger.debug(f"----------------------------------------------------------------")
        pdb.set_trace()