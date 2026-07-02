# tool_registry.py

"""Central store for all exposed system capabilities."""

import functools, inspect


class ToolRegistry:
    """Central store for all exposed system capabilities."""
    _registry = {}

    @classmethod
    def register(cls, func):
        """ToolRegistry method."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Store metadata for Agent introspection
        cls._registry[func.__name__] = {
            "func": wrapper,
            "doc": inspect.getdoc(func),
            "params": inspect.signature(func).parameters
        }
        return wrapper
    
if __name__ == "__main__":
    # Usage in a module
    @ToolRegistry.register
    def fetch_weather(location: str) -> str:
        """Fetches real-time weather data for specific location."""
        return f"Weather in {location} is 25C."

    # Agent discovery
    print(ToolRegistry._registry.keys())