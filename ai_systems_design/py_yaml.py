"""
about:
    - title: py_yaml.py
    - author: Amin Boulouma
    - description: Takes a YAML file and parses it.

i/o:
    - input: a YAML file path or YAML text
    - output: YAML Mapping in a dict format

features:
    - key, value generation
    - 

implementations details:
    - order preservation
    - element recognition

limitations:
    - parsing not yet supported:
        - lists
        - advacend YAML concepts and nesting
"""

class YAMLParser:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, yaml_file_path=None, yaml_str=None):
        self.yaml_file_path = yaml_file_path 
        self.yaml_str = yaml_str if yaml_str else self._read_yaml_file()
        self._parse()

    def _read_yaml_file(self):
        with open(self.yaml_file_path, 'r') as yaml:
            return yaml.read()
        
    def _parse(self):
        self.mapping = {}
        for line in self.yaml_str.split("\n"):
            line = line.strip()
            if not line: continue
            else:
                self.mapping[line.split(': ')[0]] = line.split(': ')[1]
                
    def get(self, key):
        return self.mapping[key]
    
    def get_mapping(self):
        return self.mapping
    
    def __str__(self):
        return f"YAMLParser(mapping={self.mapping})"
    

if __name__ == "__main__":
    yaml_str = """name: John Doe
age: 30
home: Morocco
"""
    yaml = YAMLParser(yaml_str=yaml_str)
    print(yaml.get_mapping())
    print(yaml.get('age'))

    yaml = YAMLParser(yaml_file_path='src/py_jekyll/config.yaml')
    print(yaml.get_mapping())