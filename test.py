import logging, sys

from ai_systems_design.site_generator.site_generator import SiteGenerator 
from ai_systems_design.resilient_slug_generator import JekyllFilenameController
from ai_systems_design.engine_scheduler import Task, DAG, EngineScheduler
from ai_systems_design.resilient_client_socket import ResilientClientSocket
from ai_systems_design.container_manager_client import ContainerManagerClient
from ai_systems_design.threaded_container_manager import ThreadedContainerManager
from ai_systems_design.scalable_index import ScalableIndex
from ai_systems_design.reactive_frontend import ReconcileUI, ButtonComponent
from ai_systems_design.resilient_git_rpc_client import ResilientGitRPCClient
from ai_systems_design.threaded_git_rpc_server import ThreadedGitRPCServer
from ai_systems_design.round_robin_load_balancer import RoundRobinLoadBalancer, web_node_alpha, web_node_beta, web_node_gamma
from ai_systems_design.distributed_no_sql_database import DistributedDatabase
from ai_systems_design.intent_matching_engine import IntentMatchingEngine
from ai_systems_design.realtime_redis_engine import RealtimeRedisEngine
from ai_systems_design.resilient_http_raw_client import ResilientHTTPRawClient
from ai_systems_design.concurrent_rest_engine import ConcurrentRESTEngine
from ai_systems_design.resilient_multi_threaded_server import ResilientMultiThreadedServer
from ai_systems_design.safe_yaml_parser import ConfigurationBuilder
from ai_systems_design.architecture_renderer import ArchitectureRenderer, ArchComponent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
TARGET_REPO = "https://github.com/user/repo.git"

INTENT_DATA_REPOS = {
    "greetings": {
        "keywords": ["hello", "hi", "hey", "greetings", "good day"],
        "response": "Hello! How can I assist you today? 👋"
    },
    "state_of_being": {
        "keywords": ["how are you", "hows it going", "how are things"],
        "response": "I am operating optimally. How can I help you build today?"
    },
    "identity": {
        "keywords": ["what is your name", "who are you", "your name"],
        "response": "I am a refactored automation agent running on Python."
    },
    "capabilities": {
        "keywords": ["what can you do", "help", "features", "options"],
        "response": "I can process commands, normalize inputs, and route intents."
    },
    "farewells": {
        "keywords": ["bye", "goodbye", "exit", "quit", "see ya"],
        "response": "Goodbye! Have an excellent day."
    }
}


def test_generate_site():
    base_path = 'ai_systems_design/site_generator/'
    test_path = 'test/'
    SiteGenerator(f'{base_path}layout.html', f'{base_path}config.yaml').generate_site(f'{test_path}sg_input')

def test_resilient_slug_generator():
    JekyllFilenameController().start_generator_interface()

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

def test_threaded_git_rpc_server():
    git_server = ThreadedGitRPCServer(SERVER_HOST, SERVER_PORT)
    git_server.start_server()

def test_round_robin_load_balancer():
    # Cluster nodes are registered as uniform units inside the balancing array pool
    cluster_pool = [web_node_alpha, web_node_beta, web_node_gamma]
    load_balancer = RoundRobinLoadBalancer(backend_servers=cluster_pool)

    print("\n=== Enterprise Load Balancer Core Engaged ===")
    print("Submit message payloads below to test distribution loops. Type 'exit' to halt.")

    while True:
        try:
            print("\nclient_payload> ", end="", flush=True)
            user_payload = sys.stdin.readline().strip()

            if user_payload.lower() in ("exit", "quit"):
                print("Dismantling network configuration infrastructure layers cleanly.")
                break

            if not user_payload:
                continue

            # Package transaction argument contexts to simulate web parameters
            mock_request = {"body": user_payload, "protocol": "HTTP/1.1"}
            
            # Dispatch traffic
            gateway_response = load_balancer.route_request(mock_request)
            print(f"Client Receives -> {gateway_response}")

        except (KeyboardInterrupt, SystemExit):
            print("\nSystem execution loop terminated via hardware interrupt signal.")
            break

def test_distributed_no_sql_database():
    # 1. Initialize our clustered store wrapper
    db = DistributedDatabase("production_cluster", num_shards=2)

    # 2. Establish our collection metadata layout boundaries
    users_schema = {"name": "text", "age": "int", "status": "text"}
    users = db.create_collection("users", schema=users_schema)

    # 3. Populate collection store variables
    users.insert_one({"name": "Alice", "age": 30, "status": "active"})
    users.insert_one({"name": "Bob", "age": 30, "status": "pending"})
    users.insert_one({"name": "Charlie", "age": 25, "status": "active"})

    # 4. Perform structured search query actions
    search_results = users.find({"age": 30})
    print("Search Results (age == 30):", search_results)

    # 5. Execute explicit pipeline queries (Fully functional pipeline handling)
    aggregation_pipeline = [
        {"$match": {"status": "active"}},
        {"$count": "active_users_count"}
    ]
    agg_results = users.aggregate(aggregation_pipeline)
    print("\nAggregation Framework Output:", agg_results)

    # 6. Distribute elements down onto structural data cluster partitions safely
    db.shard_collection("users", shard_key="name")
    
    for shard in db.shards:
        allocated = shard.collections.get("users", [])
        print(f"Cluster Shard #{shard.shard_id} local document count: {len(allocated)}")

def test_intent_matching_engine():
    # Instantiate engine cleanly parsing external mapping values
    engine = IntentMatchingEngine(intents=INTENT_DATA_REPOS)

    print("\n=== Robust Intent Processing Bot Interface Enabled ===")
    print("Ask questions smoothly. Type 'exit' to terminate the runtime cycle.")

    while True:
        try:
            print("\nUser> ", end="", flush=True)
            user_raw_string = sys.stdin.readline().strip()

            if user_raw_string.lower() in ("exit", "quit"):
                print("Bot: Goodbye!")
                break

            if not user_raw_string:
                continue

            bot_reply = engine.extract_response(user_raw_string)
            print(f"Bot: {bot_reply}")

        except (KeyboardInterrupt, SystemExit):
            print("\nSession killed via hardware interrupt signal.")
            break

def test_realtime_redis_engine():
    engine = RealtimeRedisEngine()
    print("\n=== Multi-Type Mock Redis Cluster Interface Engaged ===")
    print("Execute core commands [SET, GET, DEL, INCR, EXPIRE, TTL]. Type 'exit' to halt.")

    while True:
        try:
            print("\nredis-cli> ", end="", flush=True)
            input_line = sys.stdin.readline().strip()

            if input_line.lower() in ('exist', 'quit'):
                print("Halting server instance engine state cleanly.")
                break

            if not input_line:
                continue

            execution_output = engine.execute_command_string(input_line)
            print(execution_output)

        except (KeyboardInterrupt, SystemExit):
            print("\nTerminated via supervisor hardware signal line.")
            break

def test_resilient_http_raw_client():
    # Context manager pattern ensures explicit teardown safeguards apply uniformly
    try:
        with ResilientHTTPRawClient(SERVER_HOST, SERVER_PORT) as client_runtime:
            client_runtime.start_repl_loop()
    except Exception as initialization_failure:
        logger.critical(f"Failed to engage network testing suite system execution nodes: {initialization_failure}")

def test_concurrent_rest_engine():
    app = ConcurrentRESTEngine(SERVER_HOST, SERVER_PORT)
    app.start_server()

def test_resilient_multi_threaded_server():
    server = ResilientMultiThreadedServer(SERVER_HOST, SERVER_PORT)
    server.start_server()

def test_safe_yaml_parser():
    # Test Scenario A: Dynamic text stream ingestion
    raw_yaml_stream = """
    # Infrastructure Environment Allocations
    app_id: custom_microservice_node
    max_retries: 5
    api_key: 'secret_token_signature_hash'
    malformed_line_test_without_spaces
    """

    print("--- Executing Fluent Builder Construction Pipeline ---")
    config = (
        ConfigurationBuilder()
        .from_text(raw_yaml_stream)
        .build()
    )

    # FIXED: Accessing keys immediately works without needing to call any middle-tier methods first!
    print(f"Verified App ID   : {config.get('app_id')}")
    print(f"Verified API Key  : {config.get('api_key')}")
    # FIXED: Invalid configuration lines are skipped safely rather than crashing the loop
    print(f"Missing Property  : {config.get('non_existent_key', 'fallback_default_value')}")

    print("\n--- Executing Simulated File Ingestion Pipeline ---")
    file_config = ConfigurationBuilder().from_file("_config.yaml").build()
    print(f"Parsed Target Map : {file_config.to_dict()}")

def test_architecture_renderer():
        # Define system topology declaratively
    topology = ArchComponent("Load Balancer", "lb", [
        ArchComponent("API Service", "service", [
            ArchComponent("User Database", "database"),
            ArchComponent("Cache Layer", "service")
        ]),
        ArchComponent("API Service", "service", [
            ArchComponent("User Database", "database"),
            ArchComponent("Cache Layer", "service")
        ])
    ])

    renderer = ArchitectureRenderer()
    html_output = renderer.generate_html(topology)
    
    with open("test/ar_output/arch_diagram.html", "w") as f:
        f.write(html_output)
    
    logger.info("Artifact generation successful: 'arch_diagram.html' created.")

if __name__ == "__main__":
    #test_generate_site()
    test_resilient_slug_generator()
    #test_start_engine_scheduler()
    #test_resilient_client_socket()
    #test_container_manager_client()
    # #TODO - TEST FAIL - ThreadedContainerManager
    #test_threaded_container_manager()
    #test_scalable_index()
    #test_reactive_frontend()
    #test_resilient_git_rpc_client()
    #test_threaded_git_rpc_server()
    #test_round_robin_load_balancer()
    #test_distributed_no_sql_database()
    #test_intent_matching_engine()
    #test_realtime_redis_engine()
    #test_resilient_http_raw_client()
    #test_concurrent_rest_engine()
    #test_resilient_multi_threaded_server()
    #test_safe_yaml_parser()
    #test_architecture_renderer()

    pass