# test_git_rpc_server.py

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.git_rpc_server import GitRPCServer

class TestGitRPCServer(TestMixin):
    """Test the git_rpc_server module functionality."""

    def __init__(self) -> None:
        """TestGitRPCServer Constructor"""
        super().__init__()
        self.logger.info("TestGitRPCServer initialized.")

    async def test(self):
        """TestGitRPCServer Test."""
        super().test()
        SERVER_HOST = "127.0.0.1"
        GIT_RPC_SERVER_PORT = 8084
        git_server = GitRPCServer(SERVER_HOST, GIT_RPC_SERVER_PORT)
        await git_server.start_git_rpc_server()
