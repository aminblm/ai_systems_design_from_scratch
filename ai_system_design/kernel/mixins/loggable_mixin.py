import logging

class LoggableMixin:
    """Provides instant logger capability."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"[{self.__class__.__name__}] LoggableMixin initialized.")