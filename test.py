import logging, sys

from ai_systems_design.site_generator.site_generator import SiteGenerator 
from ai_systems_design.py_slug_generator import SlugGenerator, TerminalInterface
from ai_systems_design.engine_scheduler import Task, DAG, EngineScheduler
from ai_systems_design.resilient_client_socket import ResilientClientSocket
from ai_systems_design.container_manager_client import ContainerManagerClient
from ai_systems_design.threaded_container_manager import ThreadedContainerManager
from ai_systems_design.scalable_index import ScalableIndex
from ai_systems_design.reactive_frontend import ReconcileUI, ButtonComponent
from ai_systems_design.resilient_git_rpc_client import ResilientGitRPCClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
TARGET_REPO = "https://github.com/user/repo.git"


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

def test_scalable_index():
    # Initialise index schema configuration boundaries safely
    schema_config = {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "date": {"type": "date"}
        }
    }

    # Spin up an index containing 4 dinstinct shards
    search_index = ScalableIndex("production_index", schema_config, num_shards=4)

    # Ingest data targets passing distinct system ID routing handles
    search_index.add_document(document_id=101, document={
        "title": "Design Patterns", "author": "John Doe", "date": "2026-01-01"
    })
    search_index.add_document(document_id=102, document={
        "title": "Concurrent Computing", "author": "John Pie", "date": "2026-03-15"
    })
    search_index.add_document(document_id=103, document={
        "title": "Distributed Systems Handbook", "author": "John Doe", "date": "2026-05-20"
    })

    # Execute dynamic search query
    pie_query = {"term": {"author": "John Pie"}}
    doe_query = {"term": {"author": "John Doe"}}

    print("Search Results (John Pie)", search_index.search(pie_query))
    print("Search Results (John Doe)", search_index.search(doe_query))

    # Evalue aggregations
    author_aggregation = {"term": {"field": "author"}}
    print("Aggregation Results (Author):", search_index.aggregate_counts(author_aggregation))

    # Print out actual distributed allocation struction across partitions
    for shard in search_index.shards:
        print(f"Shard {shard.shard_id} allocation storage list size: {len(shard.documents)}") 

def test_reactive_frontend():
    # 1. Initialise the framework container shell
    app = ReconcileUI()

    # 2. Wire up shared event bus global listeners
    def log_click_telemetry(data): logger.info(f"[Metrics App] Tracked user interaction click event. Metadata: {data}")
    def play_sound_effect(data): logger.info(f"[Audio App] Playing click.wav asset...")

    # 3. Instantiate a strongly-typed component passing structural layout patterns
    def render_button(comp: ButtonComponent) -> str:
        disable_attr = " disabled" if comp.is_disabled else ""
        return f"<button id='{comp.name}'{disable_attr}>{comp.text}</button>"
    
    submit_button = ButtonComponent(name="submit-primary", render_fn=render_button)
    app.register_component(submit_button)

    # 4. Initial state display pass
    app.display()

    # 5. Perform runtime state mutations. Mutating directly triggers target reactivity loops!
    submit_button.text = "Processing Request..."
    submit_button.is_disabled = True

    # 6. Displaying the viez tree updates immediately reflecting the underlying changes
    app.display()

    # 7. Fire runtime event hooks
    logger.info("Simulating hardware user mouse click action targeting the component...")
    app.event.dispatch("btn_click", event_data={"cursor_x": 142, "cursor_y": 80})

def test_resilient_git_rpc_client():
    # Context manager implementation replaces sequential manual channel closes entirely
    try:
        with ResilientGitRPCClient(SERVER_HOST, SERVER_PORT) as git_agent:
            server_feedback = git_agent.dispatch_clone(repository_url=TARGET_REPO)
            print(f"\n[Execution Worker Response]: {server_feedback}")
            
    except Exception as fatal_error:
        logger.critical(f"Abrupt termination handling repository pipeline sequence tasks: {fatal_error}")


if __name__ == "__main__":
    #test_generate_site()
    #test_generate_slugs()
    #test_start_engine_scheduler()
    #test_resilient_client_socket()
    #test_container_manager_client()
    # #TODO - TEST FAIL - ThreadedContainerManager
    #test_threaded_container_manager()
    #test_scalable_index()
    #test_reactive_frontend()
    # #TODO - TEST WHEN GIT SERVER RUNNING - ResilientGitRPCClient
    test_resilient_git_rpc_client()