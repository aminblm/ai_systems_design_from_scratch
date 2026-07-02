# architecture_renderer.py
from dataclasses import dataclass
from typing import List

from ai_system_design.kernel.mixins import LoggableMixin
        
@dataclass
class ArchComponent(LoggableMixin):
    """Represents a structural node in the architecture graph."""

    def __init__(self, name: str, component_type: str, children: List['ArchComponent'] = list()) -> None:
        super().__init__()
        self.name = name
        self.component_type = component_type
        self.children = children
    

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
