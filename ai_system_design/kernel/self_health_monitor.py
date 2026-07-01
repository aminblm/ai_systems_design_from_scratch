# self_health_monitor.py
import time, threading

from ai_system_design.kernel.mixins import TestMixin, LoggableMixin


class TestSelfHealthService(TestMixin):
    """Test the self_health_monitor module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestSelfHealthService initialized.")

    def test(self):
        #TODO Proper testing of self health system
        REGISTRY = {}
        AGENT = lambda x: x

        super().test()
        health_service = SelfHealthService(REGISTRY, AGENT)
        threading.Thread(target=health_service.monitor, daemon=True)


class SelfHealthService(LoggableMixin):
    """"Monitors system health and auto-restarts failed modules."""
    def __init__(self, registry, agent):
        super().__init__()
        self.registry = registry
        self.agent = agent
        self.logger.info("SelfHealthService initialized.")

    def monitor(self):
        while True:
            for name, module in self.registry.items():
                # Heartbeat check
                if not module.is_healthy():
                    self.logger.warning(f"[HEALTH] {name} failed. Triggering recovery...")
                    self.agent.run_cycle(f"RESTART_MODULE_{name}")
            time.sleep(5)