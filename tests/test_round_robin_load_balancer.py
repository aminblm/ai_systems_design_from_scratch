# test_round_robin_load_balancer.py
import sys
from typing import Any
from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.round_robin_load_balancer import RoundRobinLoadBalancer


class TestRoundRobinLoadBalancer(TestMixin):
    """Test the round_robin_load_balancer module functionality."""

    def __init__(self) -> None:
        super().__init__()

    def test(self):
        super().test()
        
        # Refactored Backends: Interchangeable, homogeneous processors accepting generic signatures
        def web_node_alpha(context: dict[str, Any]) -> str:
            return f"Response processed by [Node Alpha]. Payload data: '{context.get('body')}'"

        def web_node_beta(context: dict[str, Any]) -> str:
            return f"Response processed by [Node Beta]. Payload data: '{context.get('body')}'"

        def web_node_gamma(context: dict[str, Any]) -> str:
            return f"Response processed by [Node Gamma]. Payload data: '{context.get('body')}'"

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
        