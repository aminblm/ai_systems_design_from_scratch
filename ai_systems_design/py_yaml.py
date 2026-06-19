from ai_systems_design.utils import FileOperationsUtility


class FileOperations:
    @staticmethod
    def read_yaml_file(yaml_file_path): return FileOperationsUtility.read_decoded(yaml_file_path)


class YAMLBuilder:
    def __init__(self):
        self.yaml_file_path = None
        self.yaml_text = None

    def set_yaml_file_path(self, yaml_file_path):
        self.yaml_file_path = yaml_file_path
        return self

    def set_yaml_text(self, yaml_text):
        self.yaml_text = yaml_text
        return self
    
    def build(self):
        return YAML(self.yaml_file_path, self.yaml_text)

    @staticmethod
    def create_default():
        return YAMLBuilder().build()
    
    @staticmethod
    def create_from_file(yaml_file_path):
        return YAMLBuilder().set_yaml_file_path(yaml_file_path).build()
    
    @staticmethod
    def create_from_text(yaml_text):
        return YAMLBuilder().set_yaml_text(yaml_text).build()
    

class YAMLParser:
    @staticmethod
    def parse(yaml_content):
        mapping = {}
        for line in yaml_content.split("\n"):
            line = line.strip()
            if not line: continue
            else: mapping[line.split(': ')[0]] = line.split(': ')[1]
        return mapping


class YAML:
    def __init__(self, yaml_file_path=None, yaml_text=None):
        self.yaml_file_path = yaml_file_path 
        self.yaml_text = yaml_text

    def get_mapping_from_file(self):
        self.mapping = YAMLParser.parse(FileOperations.read_yaml_file(self.yaml_file_path))
        return self.mapping
    
    def get_mapping_from_text(self):
        self.mapping = YAMLParser.parse(self.yaml_text)
        return self.mapping
                
    def get(self, key):
        return self.mapping[key]