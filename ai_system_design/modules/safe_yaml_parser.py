# safe_yaml_parser.py

import re
from typing import Dict, Any, Optional, Generator, Any
from pathlib import Path

from ai_system_design.kernel.utils import IOUtility
from ai_system_design.kernel.mixins import LoggableMixin

        
class SafeYAMLParser(LoggableMixin):
    """A safe textual scanner utilizing regular expressions to process configuration properties."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("SafeYAMLParser initialized.")

    def dump(self):
        """YAML dict to text"""

    def parse_to_dict(self, yaml_iterator: Generator[str, None, None]) -> Dict[str, Any]:
        """Parses flat key-value text lines, stripping comments and validating spacing."""
        
        line_num: int = 0
        mapping: Dict[str, Any] = {}

        if not yaml_iterator:
            return mapping

        for line in yaml_iterator:
            if not line or line.startswith('#'):
                line_num += 1
                continue

            # Regex isolates key from value by looking for the first colon delimiter separator
            match = re.match(r'^([^:]+):\s*(.*)$', line)
            if not match:
                self.logger.warning(f"[YAML Parser Warning] Skipping unparseable syntax on line {line_num}: '{line}'")
                line_num += 1
                continue

            key = match.group(1).strip()
            value = match.group(2).strip()

            # Clean trailing inline comments if present in value token blocks
            if '#' in value:
                value = value.split('#', 1)[0].strip()

            # Strip literal enveloping quotes from configuration values
            if value.startswith(('"', "'")) and value.endswith(('"', "'")):
                value = value[1:-1]

            mapping[key] = value

        return mapping
    

class ConfigurationEngine(LoggableMixin):
    """An immutable data container holding fully parsed application config properties."""

    def __init__(self, metadata: Dict[str, Any]) -> None:
        super().__init__()
        # Protect state by isolating properties internally
        self._config_map = metadata
        self.logger.info("ConfigurationEngine initialized.")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Fetches data properties safely while enforcing a default fallback strategy."""
        return self._config_map.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Exposes an isolated copy of the internal configuration records."""
        return self._config_map.copy()


class ConfigurationBuilder(LoggableMixin):
    """A fluent builder interface ensuring valid construction sequences for configuration engines."""

    def __init__(self) -> None:
        super().__init__()
        self._text_iterator: Optional[Generator[str, None, None]] = None
        self.logger.info("ConfigurationBuilder initialized.")

    def from_text(self, yaml_text: str) -> ConfigurationBuilder:
        """Loads configuration variables straight from a raw multi-line string sequence."""
                             
        self._text_iterator = IOUtility().text_to_lines_generator(yaml_text)
        return self

    def from_file(self, file_path: str | Path) -> ConfigurationBuilder:
        """Configuration ingestion from disk files via platform utility helpers."""
        self._text_iterator = IOUtility().text_to_lines_generator(IOUtility().read_decoded(file_path))
        return self

    def build(self) -> ConfigurationEngine:
        """Triggers parsing transformations and returns an operational config container instance."""
        if self._text_iterator is None:
            self.logger.warning("Building configuration environment with zero raw inputs. Emitting empty map.")
            return ConfigurationEngine(metadata={})

        # Parsing is executed *during* building, preventing any runtime state lookups errors
        parsed_data = SafeYAMLParser().parse_to_dict(self._text_iterator)
        return ConfigurationEngine(metadata=parsed_data)