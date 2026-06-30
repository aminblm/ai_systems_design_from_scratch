# reactive_frontend.py
from typing import Callable, Any, Dict, List

from ai_system_design.kernel.logger import logger



class ReactiveState:
    """A descriptor that intercepts mutations to enforce property-level reactivity cascades."""

    def __init__(self, default_value: Any = None) -> None:
        self._private_name = ""
        self.default_value = default_value

    def __set_name__(self, owner: Any, name: str) -> None:
        self._private_name = f"_{name}"

    def __get__(self, instance: Any, name: str) -> Any:
        if instance is None:
            return self
        return getattr(instance, self._private_name, self.default_value)
    
    def __set__(self, instance: Any, value: Any) -> None:
        old_value = getattr(instance, self._private_name, self.default_value)
        if old_value != value:
            setattr(instance, self._private_name, value)
            # If the instance has a reactivity hook, notify it of the mutation
            if hasattr(instance, "make_dirty"):
                instance.make_dirty()


class Component:
    """An isolated UI block that tracks its own reactive state variables."""

    def __init__(self, name: str, render_fn: Callable[["Component"], str]) -> None:
        self.name = name
        self._render_fn = render_fn
        self._is_dirty: ReactiveState = ReactiveState(True)
        self._cached_dom = ""

    def make_dirty(self) -> None:
        self._is_dirty = ReactiveState(True)
    
    def render(self) -> str:
        """Renders cleanly, leveraging caching unless state mutations have dirtied the view."""
        if self._is_dirty:
            logger.debug(f"State mutation caught. Re-endering component: [{self.name}]")
            self._cached_dom = self._render_fn(self)
            self.is_dirty = False
        return self._cached_dom
    

class ButtonComponent(Component):
    """Example of an explicit, strong-type reactive component subclass."""

    # Define reactive fields cleanly at class level
    text = ReactiveState("Default Button Label")
    is_disabled = ReactiveState(False)


class EventDispatcher:
    """An event broker implementating a standard multicast Observer pattern."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        """Appends a subscriber function without flattening existing tracking keys."""

        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(handler)

    def dispatch(self, event_type: str, event_data: Any = None) -> None:
        """Fires updates out safely to all registered callback hooks downstream."""
        handlers = self._listeners.get(event_type, [])
        if not handlers:
            logger.warning(f"Event '{event_type}' was dispatched but has no active subscribers.")
            return
        
        for handler in handlers:
            try:
                handler(event_data)
            except Exception as err:
                logger.error(f"Error handling event channel '{event_type}': {err}")


class ReconcileUI:
    """The master runtime shell holding layout bindings and event loops."""

    def __init__(self) -> None:
        self.components: List[Component] = []
        self.event = EventDispatcher()

    def register_component(self, component: Component) -> Component:
        self.components.append(component)
        return component
    
    def display(self) -> None:
        """Outputs the current visual state layer compilation frame."""
        print("\n--- Current Virtual DOM Frame ---")
        for component in self.components:
            print(component.render())
        print("----------------------------------")
