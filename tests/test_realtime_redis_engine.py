import sys

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.realtime_redis_engine import RealtimeRedisEngine


class TestRealtimeRedisEngine(TestMixin):
    """Test the realtime_redis_engine module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestRealtimeRedisEngine initialized.")

    def test(self):
        super().test()
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
        
