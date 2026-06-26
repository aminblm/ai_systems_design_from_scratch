"""src/__init__.py file for packaging modules and importing them within the monolith."""

import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)