import logging, re
from typing import Dict, Any, Optional

from ai_systems_design.utils import FileOperationsUtility


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class SafeYAMLParser:
    """A safe textual scanner utilizing regular expressions to process configuration properties."""

    @staticmethod
    def parse_to_dict(yaml_content: str) -> Dict[str, Any]:
        """Parses flat key-value text lines, stripping comments and validating spacing."""
        
        mapping: Dict[str, Any] = {}
        if not yaml_content:
            return mapping

        for line_num, line in enumerate(yaml_content.splitlines(), start=1):
            # Strip leading/trailing whitespaces and drop pure comments
            cleaned_line = line.strip()
            if not cleaned_line or cleaned_line.startswith('#'):
                continue

            # Regex isolates key from value by looking for the first colon delimiter separator
            match = re.match(r'^([^:]+):\s*(.*)$', cleaned_line)
            if not match:
                logger.warning(f"[YAML Parser Warning] Skipping unparseable syntax on line {line_num}: '{cleaned_line}'")
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
    

class ConfigurationEngine:
    """An immutable data container holding fully parsed application config properties."""

    def __init__(self, metadata: Dict[str, Any]) -> None:
        # Protect state by isolating properties internally
        self._config_map = metadata

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Fetches data properties safely while enforcing a default fallback strategy."""
        return self._config_map.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Exposes an isolated copy of the internal configuration records."""
        return self._config_map.copy()


class ConfigurationBuilder:
    """A fluent builder interface ensuring valid construction sequences for configuration engines."""

    def __init__(self) -> None:
        self._raw_text: Optional[str] = None

    def from_text(self, yaml_text: str) -> "ConfigurationBuilder":
        """Loads configuration variables straight from a raw multi-line string sequence."""
        self._raw_text = yaml_text
        return self

    def from_file(self, file_path: str) -> "ConfigurationBuilder":
        """Configuration ingestion from disk files via platform utility helpers."""
        self._raw_text = FileOperationsUtility.read_decoded(file_path)
        return self

    def build(self) -> ConfigurationEngine:
        """Triggers parsing transformations and returns an operational config container instance."""
        if self._raw_text is None:
            logger.warning("Building configuration environment with zero raw inputs. Emitting empty map.")
            return ConfigurationEngine(metadata={})

        # Parsing is executed *during* building, preventing any runtime state lookups errors
        parsed_data = SafeYAMLParser.parse_to_dict(self._raw_text)
        return ConfigurationEngine(metadata=parsed_data)