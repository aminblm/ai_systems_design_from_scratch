from typing import Any
from pprint import pprint
import pdb 

from ai_system_design.kernel.logger import logger


def debug(arg_name: str, arg: Any) -> None:
    logger.debug(f"----------------------------DEBUGGING---------------------------")
    pprint(f"{arg_name}={arg}")
    logger.debug(f"----------------------------------------------------------------")
    pdb.set_trace()