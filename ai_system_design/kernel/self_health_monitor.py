# self_health_monitor.py

""""Monitors system health and auto-restarts failed modules."""

import time

from ai_system_design.kernel.mixins import LoggableMixin


class SelfHealthService(LoggableMixin):
    """"Monitors system health and auto-restarts failed modules."""
    def __init__(self, registry, agent):
        super().__init__()
        self.registry = registry
        self.agent = agent

    def monitor(self):
        while True:
            for name, module in self.registry.items():
                # Heartbeat check
                if not module.is_healthy():
                    self.logger.warning(f"[HEALTH] {name} failed. Triggering recovery...")
                    self.agent.run_cycle(f"RESTART_MODULE_{name}")
            time.sleep(5)