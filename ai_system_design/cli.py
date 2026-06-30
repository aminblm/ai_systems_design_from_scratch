# cli.py
import sys, argparse

from ai_system_design.modules.site_generator.site_generator import SiteGenerator 
from ai_system_design.modules.slug_generator import JekyllFilenameController
from ai_system_design.modules.engine_scheduler import Task, DAG, EngineScheduler
from ai_system_design.kernel.socket_client import SocketClient
from ai_system_design.modules.container_manager_client import ContainerManagerClient
from ai_system_design.modules.container_manager_server import ContainerManagerServer
from ai_system_design.modules.scalable_index import ScalableIndex
from ai_system_design.modules.reactive_frontend import ReconcileUI, ButtonComponent
from ai_system_design.modules.git_rpc_client import GitRPCClient
from ai_system_design.modules.git_rpc_server import GitRPCServer
from ai_system_design.modules.round_robin_load_balancer import RoundRobinLoadBalancer, web_node_alpha, web_node_beta, web_node_gamma
from ai_system_design.modules.distributed_no_sql_database import DistributedDatabase
from ai_system_design.modules.intent_matching_engine import IntentMatchingEngine
from ai_system_design.modules.realtime_redis_engine import RealtimeRedisEngine
from ai_system_design.modules.rest_api_client import RESTAPIClient
from ai_system_design.modules.rest_api_server import RESTAPIServer
from ai_system_design.kernel.socket_server import SocketServer
from ai_system_design.modules.safe_yaml_parser import ConfigurationBuilder
from ai_system_design.modules.architecture_renderer import ArchitectureRenderer, ArchComponent
from ai_system_design.modules.process_posts import run_pipeline, Path
from ai_system_design.kernel.logger import logger
from ai_system_design.kernel.debugger import debug


SERVER_HOST = "127.0.0.1"
SOCKET_SERVER_PORT = 8080
HTTP_SERVER_PORT = 8081
CONTAINER_MANAGER_PORT = 8082
REST_API_PORT = 8083
GIT_RPC_SERVER_PORT = 8084
TARGET_REPO = "https://github.com/aminblm/ai_systems_design_from_scratch.git"

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


def generate_site():
    base_path = 'ai_system_design/site_generator/'
    test_path = 'test/'
    SiteGenerator(f'{base_path}layout.html', f'{base_path}config.yaml').generate_site(f'{test_path}sg_input')

def slug_generator():
    JekyllFilenameController().start_generator_interface()

def engine_scheduler():
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

def socket_client():
    # Using a context manager completely replaces manual tracking of .close()
    try:
        with SocketClient(SERVER_HOST, SOCKET_SERVER_PORT) as client:
            server_handshake = client.receive_message()
            if server_handshake:
                print(f"\n[Server]: {server_handshake}")

            #Collect explicit local buffer arguments
            print("\nEnter outound payload message:")
            user_input = sys.stdin.readline().strip()
        
            if user_input:
                client.send_message(user_input)
                print(client.receive_message())
    
    except (KeyboardInterrupt, SystemExit):
        logger.info("\nExecution cancelled by user signal interrupt. Exiting safely.")
    except Exception as general_failure:
        logger.critical(f"Fatal application runtime termination event: {general_failure}")

def container_manager_client():
    # Context manager auto-manages low-level cleanup on teardown or crash
    try:
        with ContainerManagerClient(SERVER_HOST, CONTAINER_MANAGER_PORT) as client:
            client.start_interface()
    except Exception as fatal_err:
        logger.critical(f"Failed to run service management shell: {fatal_err}")

def container_manager_server():
    manager = ContainerManagerServer(SERVER_HOST, CONTAINER_MANAGER_PORT)
    manager.start_container_manager_server()

def scalable_index():
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

def reactive_frontend():
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

def git_rpc_client():
    # Context manager implementation replaces sequential manual channel closes entirely
    try:
        with GitRPCClient(SERVER_HOST, GIT_RPC_SERVER_PORT) as git_agent:
            server_feedback = git_agent.dispatch_clone(repository_url=TARGET_REPO)
            print(f"\n[Execution Worker Response]: {server_feedback}")
            
    except Exception as fatal_error:
        logger.critical(f"Abrupt termination handling repository pipeline sequence tasks: {fatal_error}")

def git_rpc_server():
    git_server = GitRPCServer(SERVER_HOST, GIT_RPC_SERVER_PORT)
    git_server.start_git_rpc_server()

def round_robin_load_balancer():
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

def distributed_no_sql_database():
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

def intent_matching_engine():
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

def realtime_redis_engine():
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

def rest_api_client():
    # Context manager pattern ensures explicit teardown safeguards apply uniformly
    try:
        RESTAPIClient(SERVER_HOST, REST_API_PORT).start_repl_loop()
    except Exception as initialization_failure:
        logger.critical(f"Failed to engage network testing suite system execution nodes: {initialization_failure}")

def rest_api_server():
    app = RESTAPIServer(SERVER_HOST, REST_API_PORT)

    app.get("/test-get", "GET Test Path Registered Successfully.")
    app.post("/test-post", '{"post": "POST Test Path Registered Successfully."}')
    app.put("/test-put", '{"put": "PUT Test Path Registered Successfully."}')
    app.delete("/test-delete", 'DELETE Test Path Registred Successfully.')

    app.start_http_server()

def socket_server():
    server = SocketServer(SERVER_HOST, SOCKET_SERVER_PORT)

    server.add_middleware(lambda text: f"Middleware: {text}".encode("utf-8"))
    server.add_middleware(lambda text: f"Another Middleware: {text}".encode("utf-8"))

    server.start_socket_server()

def safe_yaml_parser():
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

def architecture_renderer():
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

def process_posts(input, output):
    run_pipeline(input, output)

def cli():
    """Example module usage: 
    python main.py --module slug_generator"""
    parser = argparse.ArgumentParser(description="AI System Design Modules")
    parser.add_argument("--module", required=True)

    # process_posts arguments
    parser.add_argument("--input", required=False, type=Path, help="Input directory containing .md files")
    parser.add_argument("--output", required=False, type=Path, help="Output directory for processed files")      
    
    args = parser.parse_args()
    match args.module:
        # Frontend
        case "reactive_frontend": reactive_frontend()

        # Load Balancing
        case "round_robin_load_balancer": round_robin_load_balancer()

        # Sockets
        case "socket_client": socket_client()
        case "socket_server": socket_server()

        # REST APIs
        case "rest_api_client": rest_api_client()
        case "rest_api_server": rest_api_server()

        # Git RPC
        case "git_rpc_client": git_rpc_client()
        case "git_rpc_server": git_rpc_server()
        
        # TODO - TEST FAIL - ContainerManager
        # cmd> run
        # Enter container name: python
        # 2026-06-26 05:14:26,834 [WARNING] Remote host has closed the connection stream channel.
        # [Server Response]:
        # Container Management
        case "container_manager_client": container_manager_client()
        case "container_manager_server": container_manager_server()

        # Databases
        case "scalable_index": scalable_index()
        case "distributed_no_sql_database": distributed_no_sql_database()
        
        # Caching
        case "realtime_redis_engine": realtime_redis_engine()

        # AI - Intent matching enging
        case "intent_matching_engine": intent_matching_engine()

        # Tasks Scheduler
        case "engine_scheduler": engine_scheduler()

        # Site / Blog Posts / Internet Content Generator
        case "generate_site": generate_site()
        case "slug_generator": slug_generator()
        case "safe_yaml_parser": safe_yaml_parser()
        case "architecture_renderer": architecture_renderer()
        case "process_posts": process_posts(args.input, args.output)

        # Edge-cases
        case _: logger.warning("Enter a valid module.")
    pass