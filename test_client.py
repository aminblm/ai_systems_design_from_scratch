import logging

from ai_systems_design.container_manager_client import ContainerManagerClient
from ai_systems_design.resilient_git_rpc_client import ResilientGitRPCClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
TARGET_REPO = "https://github.com/user/repo.git"

def test_container_manager_client():
    # Context manager auto-manages low-level cleanup on teardown or crash
    try:
        with ContainerManagerClient(SERVER_HOST, SERVER_PORT) as client:
            client.start_interface()
    except Exception as fatal_err:
        logger.critical(f"Failed to run service management shell: {fatal_err}")

def test_resilient_git_rpc_client():
    # Context manager implementation replaces sequential manual channel closes entirely
    try:
        with ResilientGitRPCClient(SERVER_HOST, SERVER_PORT) as git_agent:
            server_feedback = git_agent.dispatch_clone(repository_url=TARGET_REPO)
            print(f"\n[Execution Worker Response]: {server_feedback}")
            
    except Exception as fatal_error:
        logger.critical(f"Abrupt termination handling repository pipeline sequence tasks: {fatal_error}")


if __name__ == "__main__":
    # #TODO - TEST FAIL - ContainerManagerClient
    #test_container_manager_client()
    test_resilient_git_rpc_client()