from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.architecture_renderer import ArchComponent, ArchitectureRenderer


class TestArchitectureRenderer(TestMixin):
    """Test the architecture_renderer module functionality."""

    def __init__(self) -> None:
        super().__init__()

    def test(self):
        super().test()
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

    