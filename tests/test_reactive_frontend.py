from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.reactive_frontend import ReconcileUI, ButtonComponent

        
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

