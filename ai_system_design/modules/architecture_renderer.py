# architecture_renderer.py
from dataclasses import dataclass, field
from typing import List

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestArchitectureRenderer(TestMixin):
    """Test the architecture_renderer module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestArchitectureRenderer initialized.")

    def test_architecture_renderer(self):
        # Define system topology declaratively
        topology = ArchComponent("Load Balancer", "lb", [
            ArchComponent("API Service", "service", [
                ArchComponent("User Database", "database"),
                ArchComponent("Cache Layer", "service")
            ]),
            ArchComponent("API Service", "service", [
                ArchComponent("User Database", "database"),
                ArchComponent("Cache Layer", "service")
            ])
        ])

        renderer = ArchitectureRenderer()
        html_output = renderer.generate_html(topology)
        
        with open("test/ar_output/arch_diagram.html", "w") as f:
            f.write(html_output)
        
        self.logger.info("Artifact generation successful: 'arch_diagram.html' created.")    

        
@dataclass
class ArchComponent(LoggableMixin):
    """Represents a structural node in the architecture graph."""

    def __init__(self, name: str, component_type: str, children: List['ArchComponent'] = list()) -> None:
        super().__init__()
        self.name = name
        self.component_type = component_type
        self.children = children
        self.logger.info("ArchComponent initialized.")
    

class ArchitectureRenderer(LoggableMixin):
    """Translates high-level component graphs into rendered HTML/CSS media."""

    CSS = """
    .arch-container { display: grid; gap: 20px; padding: 20px; font-family: sans-serif; margin: 10px;}
    .component { border: 2px solid #333; padding: 15px; border-radius: 8px; background: #f4f4f4; margin: 10px;}
    .type-service { border-color: #2ecc71; margin: 10px;}
    .type-database { border-color: #e74c3c; background: #fdf2f2; margin: 10px;}
    .label { font-weight: bold; margin-bottom: 10px; display: block; margin: 10px;}
    """

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("ArchitectureRenderer initialized.")

    def generate_html(self, root: ArchComponent) -> str:
        return f"""
        <html>
            <head><style>{self.CSS}</style></head>
            <body>
                <div class="arch-container">
                    {self._render_node(root)}
                </div>
            </body>
        </html>
        """

    def _render_node(self, node: ArchComponent) -> str:
        child_html = "".join([self._render_node(c) for c in node.children])
        return f"""
        <div class="component type-{node.component_type}">
            <span class="label">{node.name}</span>
            {child_html}
        </div>
        """
