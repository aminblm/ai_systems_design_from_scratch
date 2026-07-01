# infrastructure_as_code.py
from ai_system_design.modules.safe_yaml_parser import ConfigurationBuilder
from ai_system_design.kernel.mixins import LoggableMixin


class InfrastructureAsCode(LoggableMixin):
    def __init__(self, manifest_path):
        super().__init__()
        self.config = self._load_manifest(manifest_path)
        self.registry = {}
        self.logger.info("InfrastructureAsCode initialized.")
    
    def _load_manifest(self, path):
        return ConfigurationBuilder().from_file(path).build().to_dict()
    
    def bootstrap(self):
        """Dynamic instanciation based on the manifest."""
        for module_name, settings in self.config["modules"].items():
            # Dynamically instanciate based on config
            if settings["enabled"]:
                self.registry[module_name] = self._create_instance(module_name, settings)
                self.logger.info(f"[BOOTSTRAP] Initialised {module_name} in {settings['mode']} mode.")

    def _create_instance(self, module_name, settings):
        pass

#TODO proper testing of IaC
# topology.yaml
# modules:
#   db: { enabled: true, mode: "sharded" }
#   logger: { enabled: true, mode: "verbose" }