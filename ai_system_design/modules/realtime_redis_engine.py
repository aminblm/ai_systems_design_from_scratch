# realtime_redis_engine.py
import time, sys
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Callable

from ai_system_design.kernel.mixins import TestMixin, LoggableMixin


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
        

@dataclass
class RedisObject(LoggableMixin):
    """An internal storage wrapper holding an explicit data payload and its eviction metadata."""
    value: Any
    expires_at: Optional[float] = None # Epoch timestamp representing absolute death boundary

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("RedisObject initialized.")

    def is_expired(self) -> bool:
        """Determines if the instance has surpassed its chronological survival window."""
        if self.expires_at is None:
            return False
        return time.time() >= self.expires_at


class RealtimeRedisEngine(LoggableMixin):
    """A type-safe, resilient in-memory data store replacing key Redis operations."""

    def __init__(self) -> None:
        super().__init__()
        # A flat unified namespace map matches Redis's core architecture
        self._db: Dict[str, RedisObject] = {}
        self.logger.info("RealtimeRedisEngine initialized.")

    def _get_valid_obj(self, key: str) -> Optional[RedisObject]:
        """Fetches a record dynamically while perfoming passive lazy eviction pruning."""
        obj = self._db.get(key)
        if not obj:
            return None
        
        if obj.is_expired():
            self.logger.info(f"[Lazy Eviction] Key '{key}' has passed its TTL threshold.")
            del self._db[key]
            return None
        
        return obj
    
    def set(self, args: List[str]) -> str:
        if len(args) < 2: return "ERR wrong number of arguments for 'set' command"
        key, value = args[0], args[1]
        self._db[key] = RedisObject(value=value)
        return "OK" 

    def get(self, args: List[str]) -> str:
        if len(args) < 1: return "ERR wrong number of arguments for 'get' command"
        obj = self._get_valid_obj(args[0])
        return f"'{obj.value}'" if obj else "(nil)" 
    
    def delete(self, args: List[str]) -> str:
        if len(args) < 1: return "ERR wrong number of arguments for 'delete' command"
        count = 0
        for key in args:
            if self._get_valid_obj(key):
                del self._db[key]
                count += 1
        return f"(integer) {count}"

    def incr(self, args: List[str]) -> str:
        if len(args) < 1: return "ERR wrong number of arguments for 'incr' command"
        obj = self._get_valid_obj(args[0])

        if not obj:
            # Redis default rule: initialise missing keys to  1 on INCR execution
            return "(integer) 1"
        try:
            current_val = int(obj.value)
            new_val = current_val + 1
            obj.value = new_val # Persist transaction modifications back to memory
            return f"(integer) {new_val}"
        except (ValueError, TypeError):
            return "ERR value is not an integer or out of range"
    
    def expire(self, args: List[str]) -> str:
        if len(args) < 2: return "ERR wrong number of arguments for 'expire' command"
        key, seconds_str, obj = args[0], args[1], self._get_valid_obj(args[0])
        
        if not obj:
            return "(integer) 0"
        
        try:
            duration = float(seconds_str)
            obj.expires_at = time.time() + duration
            return "(integer) 1"
        except ValueError:
            return "ERR value is not a valid float interval"
    
    def ttl(self, args: List[str]) -> str:
        if len(args) < 1: return "ERR wrong number of arguments for 'ttl' command"
        key, obj = args[0], self._get_valid_obj(args[0])

        if not obj:
            return "(integer) -2" # Key does not exist or has expired already
        
        if obj.expires_at is None:
            return "(integer) -1" # Key exists but has no associated timeout expiry limit
        
        remaining_time = int(round(obj.expires_at - time.time()))
        return f"(integer) {max(0, remaining_time)}"

    def execute_command_string(self, raw_command_line: str) -> str:
        """Parses raw text words into a multi-token signature mapping block."""
        parts = raw_command_line.strip().split()
        if not parts: return ""

        cmd_token, cmd_args = parts[0].upper(), parts[1:]

        # Dynamic strategy command routing
        command_map: Dict[str, Callable[[List[str]], str]] = {
            "SET": self.set,
            "GET": self.get,
            "DEL": self.delete,
            "INCR": self.incr,
            "EXPIRE": self.expire,
            "TTL": self.ttl,
        }

        handler = command_map.get(cmd_token)
        if not handler: return f"ERR unknown command '{cmd_token}'"

        try:
            return handler(cmd_args)
        except Exception as err:
            return f"ERR execution pipeline fault: {err}"