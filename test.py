import logging, sys

from ai_systems_design.site_generator.site_generator import SiteGenerator 
from ai_systems_design.py_slug_generator import SlugGenerator, TerminalInterface
from ai_systems_design.engine_scheduler import Task, DAG, EngineScheduler
from ai_systems_design.resilient_client_socket import ResilientClientSocket
from ai_systems_design.container_manager_client import ContainerManagerClient
from ai_systems_design.threaded_container_manager import ThreadedContainerManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080


def test_generate_site():
    base_path = 'ai_systems_design/site_generator/'
    test_path = 'test/'
    SiteGenerator(f'{base_path}layout.html', f'{base_path}config.yaml').generate_site(f'{test_path}sg_input')

def test_generate_slugs():
    slug_engine = SlugGenerator()
    interface = TerminalInterface(generator=slug_engine)
    interface.run()

def test_start_engine_scheduler():
    # Define clean decoupled topology
    sample_dag = DAG("Production_pipeline")

    def extract(): logger.info("[DB] Extracting raw ingestion assets...")
    def transform(): logger.info("[Spark] Normalizing structural records...")
    def load(): logger.info("[Warehouse] Committing target delta changes...")

    task_a = Task("Extract_Data", execute_func=extract, interval_seconds=3)
    task_b = Task("Transform_Data", execute_func=transform, interval_seconds=3, upstream_dependencies={"Extract_Data"})
    task_c = Task("Load_Data", execute_func=load, interval_seconds=3, upstream_dependencies={"Transform_Data"})

    sample_dag.add_task(task_a)
    sample_dag.add_task(task_b)
    sample_dag.add_task(task_c)

    scheduler = EngineScheduler(sample_dag)
    # Run the execution agent loop
    scheduler.run_forever(tick_rate_seconds=0.5)

def test_resilient_client_socket():
    # Using a context manager completely replaces manual tracking of .close()
    try:
        with ResilientClientSocket(SERVER_HOST, SERVER_PORT) as client:
            server_handshake = client.receive_message()
            if server_handshake:
                print(f"\n[Server]: {server_handshake}")

            #Collect explicit local buffer arguments
            print("\nEnter outound payload message:")
            user_input = sys.stdin.readline().strip()
        
            if user_input:
                client.send_message(user_input)
    
    except (KeyboardInterrupt, SystemExit):
        logger.info("\nExecution cancelled by user signal interrupt. Exiting safely.")
    except Exception as general_failure:
        logger.critical(f"Fatal application runtime termination event: {general_failure}")

def test_container_manager_client():
    # Context manager auto-manages low-level cleanup on teardown or crash
    try:
        with ContainerManagerClient(SERVER_HOST, SERVER_PORT) as client:
            client.start_interface()
    except Exception as fatal_err:
        logger.critical(f"Failed to run service management shell: {fatal_err}")

def test_threaded_container_manager():
    manager = ThreadedContainerManager(SERVER_HOST, SERVER_PORT)
    manager.start_server()


if __name__ == "__main__":
    #test_generate_site()
    #test_generate_slugs()
    #test_start_engine_scheduler()
    #test_resilient_client_socket()
    #test_container_manager_client()
    # #TODO - TEST FAIL
    test_threaded_container_manager()