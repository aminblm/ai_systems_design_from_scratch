from ai_system_design.modules.container_manager_client import ContainerManagerClient
from ai_system_design.kernel.mixins import TestMixin


class TestContainerManagerClient(TestMixin):
    """Test the container_manager_client module functionality."""

    def __init__(self) -> None:
        super().__init__()

    def test(self):
        super().test()
        #TODO - TEST FAIL - ContainerManager
        # cmd> run
        # Enter container name: python
        # 2026-06-26 05:14:26,834 [WARNING] Remote host has closed the connection stream channel.
        # [Server Response]:
        # Container Management
        
        SERVER_HOST = "127.0.0.1"
        CONTAINER_MANAGER_PORT = 8082
        # Context manager auto-manages low-level cleanup on teardown or crash
        try:
            with ContainerManagerClient(SERVER_HOST, CONTAINER_MANAGER_PORT) as client:
                client.start_interface()
        except Exception as fatal_err:
            self.logger.critical(f"Failed to run service management shell: {fatal_err}")
        
