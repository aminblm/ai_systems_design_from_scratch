# utils.py
from typing import Generator
from pathlib import Path 

from ai_system_design import logger

class IOUtility:
    """Provides atomic, type-safe filesystem I/O operations with explicit encoding safeguards."""

    @staticmethod
    def text_to_lines_generator(text: str, strip=True) -> Generator[str, None, None]:
        if strip:
            for line in iter(text.splitlines()): yield line.strip()
        else: 
            for line in iter(text.splitlines()): yield line
    
    @staticmethod
    def read_decoded(file_path: str | Path, encoding: str = 'utf-8', errors: str = 'replace') -> str:
        """Reads a filesystem file safely, handling decoding anomalies with fallback flags."""
        try:
            with open(file_path, mode='rb') as target_file:
                return target_file.read().decode(encoding, errors=errors)
        except FileNotFoundError:
            logger.error(f"IO Failure: Targeted file asset path not found: '{file_path}'")
            raise
        except Exception as error:
            logger.error(f"Unexpected file system read execution error on path '{file_path}': {error}")
            raise

    @staticmethod
    def write_encoded(file_path: str | Path, content_generator: Generator[str, None, None], encoding: str = 'utf-8') -> None:
        """Writes text strings directly to disk storage volumes using strict encoding formats."""
        try:
            with open(file_path, mode='wb') as target_file:
                for line in content_generator:
                    binary_payload = (line + "\n").encode(encoding)
                    target_file.write(binary_payload)
        except Exception as error:
            logger.error(f"Unexpected file system write execution error on path '{file_path}': {error}")
            raise
