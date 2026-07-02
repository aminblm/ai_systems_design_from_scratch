
#TODO #ISSUE #2 Move datastructures to this file (i.e. shard, etc.)

from ai_system_design.kernel.mixins import LoggableMixin


class Tensor(LoggableMixin):
    """Class for the Tensor Data Structure"""
    
    def __init__(self) -> None:
        super().__init__()

class Array(LoggableMixin):
    """Class for the Array Data Structure"""

    def __init__(self) -> None:
        super().__init__()
