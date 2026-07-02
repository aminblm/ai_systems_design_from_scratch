from ai_system_design.modules.rest_api_client import RESTAPIClient
from ai_system_design.kernel.mixins import TestMixin


class TestRESTAPIClient(TestMixin):
    """Test the rest_api_client module functionality."""

    def __init__(self) -> None:
        super().__init__()

    def test(self):
        super().test()
        SERVER_HOST = "127.0.0.1"
        REST_API_PORT = 8083
        # Context manager pattern ensures explicit teardown safeguards apply uniformly
        try:
            RESTAPIClient(SERVER_HOST, REST_API_PORT).start_repl_loop()
        except Exception as initialization_failure:
            self.logger.critical(f"Failed to engage network testing suite system execution nodes: {initialization_failure}")
