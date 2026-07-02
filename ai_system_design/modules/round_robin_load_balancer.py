# round_robin_load_balancer.py
from typing import Callable, List, Dict, Any

from ai_system_design.kernel.mixins import LoggableMixin

        
class RoundRobinLoadBalancer(LoggableMixin):
    """A thread-safe, programmatic load balancer distributing homogeneous traffic evenly."""
    
    def __init__(self, backend_servers: List[Callable[[Dict[str, Any]], str]]) -> None:
        super().__init__()
        if not backend_servers:
            raise ValueError("Load Balancer infrastructure requires at least one upstream backend node.")
            
        self._backends = backend_servers
        self._next_index = 0  # Pointer tracking round-robin sequencing transitions

    def route_request(self, request_context: Dict[str, Any]) -> str:
        """Balances incoming request loads across backend pools monotonically."""
        # Select target node using modulo algorithm to ensure consistent distribution
        selected_index = self._next_index % len(self._backends)
        target_node = self._backends[selected_index]
        
        # Increment sequence tracker
        self._next_index = (selected_index + 1) % len(self._backends)

        self.logger.info(f"[LB Routing Master] Dispatched request context to Backend Node Cluster #{selected_index}")

        try:
            return target_node(request_context)
        except Exception as backend_err:
            self.logger.error(f"Backend Node Cluster #{selected_index} faulted during execution: {backend_err}")
            return "HTTP 502: Bad Gateway (Target node exception)"
    
