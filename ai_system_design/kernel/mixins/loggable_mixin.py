"""Provides instant logger capability."""

import logging

class LoggableMixin:
    """Provides instant logger capability."""
    def __init__(self, verbose: bool = False, debug: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbose = verbose
        if debug:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
        else:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"[{self.__class__.__name__}] Logger initialized.")
