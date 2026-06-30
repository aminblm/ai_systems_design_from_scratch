# reactive_frontend.py
from typing import Callable, Any, Dict, List

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin

        
class TestReactiveFrontent(TestMixin):
    """Test the reactive_frontend module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestReactiveFrontent initialized.")

    def test(self):
        super().test()
        # 1. Initialise the framework container shell
        app = ReconcileUI()

        # 2. Wire up shared event bus global listeners
        def log_click_telemetry(data): self.logger.info(f"[Metrics App] Tracked user interaction click event. Metadata: {data}")
        def play_sound_effect(data): self.logger.info(f"[Audio App] Playing click.wav asset...")

        # 3. Instantiate a strongly-typed component passing structural layout patterns
        def render_button(comp: ButtonComponent) -> str:
            disable_attr = " disabled" if comp.is_disabled else ""
            return f"<button id='{comp.name}'{disable_attr}>{comp.text}</button>"
        
        submit_button = ButtonComponent(name="submit-primary", render_fn=render_button)
        app.register_component(submit_button)

        # 4. Initial state display pass
        app.display()

        # 5. Perform runtime state mutations. Mutating directly triggers target reactivity loops!
        submit_button.text = "Processing Request..."
        submit_button.is_disabled = True

        # 6. Displaying the viez tree updates immediately reflecting the underlying changes
        app.display()

        # 7. Fire runtime event hooks
        self.logger.info("Simulating hardware user mouse click action targeting the component...")
        app.event.dispatch("btn_click", event_data={"cursor_x": 142, "cursor_y": 80})


class ReactiveState(LoggableMixin):
    """A descriptor that intercepts mutations to enforce property-level reactivity cascades."""

    def __init__(self, default_value: Any = None) -> None:
        super().__init__()
        self._private_name = ""
        self.default_value = default_value
        self.logger.info("ReactiveState initialized.")

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


class Component(LoggableMixin):
    """An isolated UI block that tracks its own reactive state variables."""

    def __init__(self, name: str, render_fn: Callable[["Component"], str]) -> None:
        super().__init__()
        self.name = name
        self._render_fn = render_fn
        self._is_dirty: ReactiveState = ReactiveState(True)
        self._cached_dom = ""
        self.logger.info("Component initialized.")

    def make_dirty(self) -> None:
        self._is_dirty = ReactiveState(True)
    
    def render(self) -> str:
        """Renders cleanly, leveraging caching unless state mutations have dirtied the view."""
        if self._is_dirty:
            self.logger.debug(f"State mutation caught. Re-endering component: [{self.name}]")
            self._cached_dom = self._render_fn(self)
            self.is_dirty = False
        return self._cached_dom


class ButtonComponent(Component, LoggableMixin):
    """Example of an explicit, strong-type reactive component subclass."""

    def __init__(self, name: str, render_fn: Callable) -> None:
        super().__init__(name, render_fn)
        self.logger.info("ButtonComponent initialized.")

    # Define reactive fields cleanly at class level
    text = ReactiveState("Default Button Label")
    is_disabled = ReactiveState(False)


class EventDispatcher(LoggableMixin):
    """An event broker implementating a standard multicast Observer pattern."""

    def __init__(self) -> None:
        super().__init__()
        self._listeners: Dict[str, List[Callable[[Any], None]]] = {}
        self.logger.info("EventDispatcher initialized.")

    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        """Appends a subscriber function without flattening existing tracking keys."""

        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(handler)

    def dispatch(self, event_type: str, event_data: Any = None) -> None:
        """Fires updates out safely to all registered callback hooks downstream."""
        handlers = self._listeners.get(event_type, [])
        if not handlers:
            self.logger.warning(f"Event '{event_type}' was dispatched but has no active subscribers.")
            return
        
        for handler in handlers:
            try:
                handler(event_data)
            except Exception as err:
                self.logger.error(f"Error handling event channel '{event_type}': {err}")


class ReconcileUI(LoggableMixin):
    """The master runtime shell holding layout bindings and event loops."""

    def __init__(self) -> None:
        super().__init__()
        self.components: List[Component] = []
        self.event = EventDispatcher()
        self.logger.info("ReconcileUI initialized.")

    def register_component(self, component: Component) -> Component:
        self.components.append(component)
        return component
    
    def display(self) -> None:
        """Outputs the current visual state layer compilation frame."""
        print("\n--- Current Virtual DOM Frame ---")
        for component in self.components:
            print(component.render())
        print("----------------------------------")
