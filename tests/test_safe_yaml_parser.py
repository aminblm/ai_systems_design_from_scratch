# test_safe_yaml_parser.pyh

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.safe_yaml_parser import ConfigurationBuilder


class TestSafeYAMLParser(TestMixin):
    """Test the safe_yaml_parser module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestSafeYAMLParser initialized.")

    def test(self):
        super().test()
        # Test Scenario A: Dynamic text stream ingestion
        raw_yaml_stream = """
        # Infrastructure Environment Allocations
        app_id: custom_microservice_node
        max_retries: 5
        api_key: 'secret_token_signature_hash'
        malformed_line_test_without_spaces
        """

        self.logger.info("--- Executing Fluent Builder Construction Pipeline ---")
        config = (
            ConfigurationBuilder()
            .from_text(raw_yaml_stream)
            .build()
        )

        # FIXED: Accessing keys immediately works without needing to call any middle-tier methods first!
        self.logger.info(f"Verified App ID   : {config.get('app_id')}")
        self.logger.info(f"Verified API Key  : {config.get('api_key')}")
        # FIXED: Invalid configuration lines are skipped safely rather than crashing the loop
        self.logger.info(f"Missing Property  : {config.get('non_existent_key', 'fallback_default_value')}")

        self.logger.info("\n--- Executing Simulated File Ingestion Pipeline ---")
        file_config = ConfigurationBuilder().from_file("_config.yaml").build()
        self.logger.info(f"Parsed Target Map : {file_config.to_dict()}")
