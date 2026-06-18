import os

from ai_systems_design.py_yaml import YAMLParser
from ai_systems_design.py_markdown_to_html.py_markdown_to_html import MarkdownToHTML


class DependencyFactory:
    @staticmethod
    def get_layout(layout_path):
        with open(layout_path, 'rb') as l: return l.read().decode('utf-8')

    @staticmethod
    def get_config_mapping(config_file_path):
        return YAMLParser(config_file_path).get_mapping()
    
    @staticmethod
    def render_layout(layout, config):
        for key in config: layout = layout.replace('{{ site.' + key + ' }}', config[key])
        return layout
    
    @staticmethod
    def get_html_content(markdown_file_path):
        return MarkdownToHTML(markdown_file_path).md_to_html()
    
    @staticmethod
    def get_dependencies(layout_path, config_file_path):
        return DependencyFactory.get_layout(layout_path), DependencyFactory.get_config_mapping(config_file_path)

    @staticmethod
    def get_file_paths(md_file_name, input_folder, output_folder):
        html_file_name = f"{ md_file_name.split('.md')[0] }.html"
        return tuple(map(lambda x, y: os.path.join(x, y), (input_folder, output_folder), (md_file_name, html_file_name)))
    
class Jekyll:
    def __init__(self, input_folder, output_folder, layout_path, config_file_path):
        self.input_folder, self.output_folder = input_folder, output_folder 
        self.layout_path, self.config_file_path = layout_path, config_file_path

    def generate_site(self):
        layout, config = DependencyFactory.get_dependencies(self.layout_path, self.config_file_path)
        for md_file_name in os.listdir(self.input_folder):
            md_file_path, html_file_path = DependencyFactory.get_file_paths(md_file_name, self.input_folder, self.output_folder)
            config['content'] = DependencyFactory.get_html_content(md_file_path)
            if os.path.isfile(md_file_path): self._generate_html_page(layout, config, html_file_path)
        print("Site generated.")

    
    def _generate_html_page(self, layout, config, html_file_path):
        layout = DependencyFactory.render_layout(layout, config)
        with open(html_file_path, 'wb') as html: html.write(layout.encode('utf-8'))
