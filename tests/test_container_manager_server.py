# test_container_manager_server.py

from ai_system_design.modules.container_manager_server import ContainerManagerServer
from ai_system_design.kernel.mixins import TestMixin


class TestContainerManagerServer(TestMixin):
    """Test the container_manager_server module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("ContainerManagerServer initialized.")

    async def test(self):
        super().test()
        SERVER_HOST = "127.0.0.1"
        CONTAINER_MANAGER_PORT = 8082

        manager = ContainerManagerServer(SERVER_HOST, CONTAINER_MANAGER_PORT)
        await manager.start_container_manager_server()

