import sys, argparse

from ai_system_design.modules.round_robin_load_balancer import RoundRobinLoadBalancer, web_node_alpha, web_node_beta, web_node_gamma
from ai_system_design.modules.architecture_renderer import ArchitectureRenderer, ArchComponent
from ai_system_design.modules.process_posts import run_pipeline
from ai_system_design.kernel.debugger import test_debugger


SERVER_HOST = "127.0.0.1"
SOCKET_SERVER_PORT = 8080
HTTP_SERVER_PORT = 8081
CONTAINER_MANAGER_PORT = 8082
REST_API_PORT = 8083
GIT_RPC_SERVER_PORT = 8084
TARGET_REPO = "https://github.com/aminblm/ai_systems_design_from_scratch.git"

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

def test_process_posts():
    """Example usage> python test.py --input _posts/20260623-in --output _posts/20260623-out"""
    parser = argparse.ArgumentParser(description="Inject metadata and links into Markdown posts.")
    parser.add_argument("--input", required=True, help="Input directory containing markdown files")
    parser.add_argument("--output", required=True, help="Output directory for processed files")
    
    args = parser.parse_args()
    #process_posts(args.input, args.output)
    #clean_posts(args.input, args.output)
    #clean_author(args.input, args.output)

def test_modules():
    """Example testing module: 
    python test.py --test slug_generator"""

    parser = argparse.ArgumentParser(description="Test AI Systems Design")
    parser.add_argument("--test", required=True)
    args = parser.parse_args()

    match args.test:
        # Frontend
        case "reactive_frontend": 
            from ai_system_design.modules.reactive_frontend import TestReactiveFrontent
            TestReactiveFrontent().test_reactive_frontend()

        # Load Balancing
        case "round_robin_load_balancer": test_round_robin_load_balancer()

        # Sockets
        case "socket_server": 
            from ai_system_design.kernel.socket_server import TestSocketServer
            TestSocketServer().test_socket_server()
        case "socket_client": 
            from ai_system_design.kernel.socket_client import TestSocketClient
            TestSocketClient().test_socket_client()

        # REST APIs
        case "rest_api_client": 
            from ai_system_design.modules.rest_api_client import TestRESTAPIClient
            TestRESTAPIClient().test_rest_api_client()
        case "rest_api_server": 
            from ai_system_design.modules.rest_api_server import TestRESTAPIServer
            TestRESTAPIServer().test_rest_api_server()

        # Git RPC
        case "git_rpc_client": 
            from ai_system_design.modules.git_rpc_client import TestGitRPCClient
            TestGitRPCClient().test_git_rpc_client()
        case "git_rpc_server": 
            from ai_system_design.modules.git_rpc_server import TestGitRPCServer
            TestGitRPCServer().test_git_rpc_server()

        # Container Management
        case "container_manager_client": 
            from ai_system_design.modules.container_manager_client import TestContainerManagerClient
            TestContainerManagerClient().test_container_manager_client()
        case "container_manager_server": 
            from ai_system_design.modules.container_manager_server import TestContainerManagerServer
            TestContainerManagerServer().test_container_manager_server()

        # Databases
        case "scalable_index": 
            from ai_system_design.modules.scalable_index import TestScalableIndex
            TestScalableIndex().test_scalable_index()
        case "distributed_no_sql_database": 
            from ai_system_design.modules.distributed_no_sql_database import TestDistributedNoSQLDatabase
            TestDistributedNoSQLDatabase().test_distributed_no_sql_database()
        
        # Caching
        case "realtime_redis_engine": 
            from ai_system_design.modules.realtime_redis_engine import TestRealtimeRedisEngine
            TestRealtimeRedisEngine().test_realtime_redis_engine()

        # AI - Intent matching enging
        case "intent_matching_engine": 
            from ai_system_design.modules.intent_matching_engine import TestIntentMatchingEngine
            TestIntentMatchingEngine().test_intent_matching_engine()

        # Tasks Scheduler
        case "engine_scheduler": 
            from ai_system_design.modules.engine_scheduler import TestEngineScheduler
            TestEngineScheduler().test_engine_scheduler()

        # Site / Blog Posts / Internet Content Generator
        case "generate_site": 
            from ai_system_design.modules.site_generator.site_generator import TestGenerateSite 
            TestGenerateSite().test_generate_site()
        case "slug_generator": 
            from ai_system_design.modules.slug_generator import TestSlugGenerator
            TestSlugGenerator().test_slug_generator()
        case "safe_yaml_parser": 
            from ai_system_design.modules.safe_yaml_parser import TestSafeYAMLParser
            TestSafeYAMLParser().test_safe_yaml_parser()
        case "architecture_renderer": test_architecture_renderer()
        case "process_posts": test_process_posts()

        # Deugger
        case "debugger": test_debugger()

        # Edge-cases
        case _:
            # TODO Edge-case proper handling 
            # logger.warning("Enter a valid test case.") 
            pass
    pass