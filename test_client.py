import logging

from ai_systems_design.container_manager_client import ContainerManagerClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

def test_container_manager_client():
    # Context manager auto-manages low-level cleanup on teardown or crash
    try:
        with ContainerManagerClient(SERVER_HOST, SERVER_PORT) as client:
            client.start_interface()
    except Exception as fatal_err:
        logger.critical(f"Failed to run service management shell: {fatal_err}")


if __name__ == "__main__":
    # #TODO - TEST FAIL - ContainerManagerClient
    test_container_manager_client()