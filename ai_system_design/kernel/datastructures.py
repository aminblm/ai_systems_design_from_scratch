# datastructures.py

from ai_system_design.kernel.mixins import LoggableMixin


class Tensor(LoggableMixin):
    """Class for the Tensor Data Structure"""
    
    def __init__(self) -> None:
        super().__init__()
        self.logger.info("Tensor initialized.")

class Array(LoggableMixin):
    """Class for the Array Data Structure"""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("Array initialized.")
