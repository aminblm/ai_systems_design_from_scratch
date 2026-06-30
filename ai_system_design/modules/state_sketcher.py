# state_sketcher.py

"""State Sketcher Tracks and records state transitions for visualization."""

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin
from ai_system_design.kernel.debugger import Debugger


class TestStateSketcher(TestMixin, LoggableMixin):
    """Test the state_sketcher module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestStateSketcher initialized.")
    
    def test(self):
        super().test()
        #TODO Test State Sketcher


class StateSketcher(LoggableMixin):
    """Tracks and records state transitions for visualization."""
    def __init__(self, target_object):
        super().__init__()
        self.target = target_object
        self.history = []

    def log_transition(self, method_name, from_state, to_state): 
        """Log the object sketch metadata."""
        self.history.append({
            "step": len(self.history) + 1,
            "action": method_name,
            "from": from_state,
            "to": to_state
        })

    def export_sketch(self): 
        """Generates text-based flow sketches."""
        print("--- State Flow Blueprint ---")
        for entry in self.history:
            print("[{}] --({})--> [{}]".format(entry['from'], entry['action'], entry['to']))


# Integration pattern
def sketch(func):
    def wrapper(self, *arg, **kwargs):
        old_state = getattr(self, "state", "init")
        result = func(self, *arg, **kwargs)
        new_state = getattr(self, "state", "unknown")
        if hasattr(self, "_sketcher"):
            self._sketcher.log_transition(func.__name__, old_state, new_state)
            StateSketcher.export_sketch(self)
        return result
    return wrapper