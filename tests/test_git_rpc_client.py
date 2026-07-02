from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.git_rpc_client import GitRPCClient

class TestGitRPCClient(TestMixin):
    """Test the git_rpc_client module functionality."""

    def __init__(self) -> None:
        """TestGitRPCClient Constructor."""
        super().__init__()

    def test(self):
        """TestGitRPCClient Test."""
        super().test()
        SERVER_HOST = "127.0.0.1"
        GIT_RPC_SERVER_PORT = 8084
        TARGET_REPO = "https://github.com/aminblm/ai_systems_design_from_scratch.git"

        # Context manager implementation replaces sequential manual channel closes entirely
        try:
            with GitRPCClient(SERVER_HOST, GIT_RPC_SERVER_PORT) as git_agent:
                server_feedback = git_agent.dispatch_clone(repository_url=TARGET_REPO)
                print(f"\n[Execution Worker Response]: {server_feedback}")
                
        except Exception as fatal_error:
            self.logger.critical(f"Abrupt termination handling repository pipeline sequence tasks: {fatal_error}")
   