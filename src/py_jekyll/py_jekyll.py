import os

from .. import py_yaml
from ..py_markdown_to_html import py_markdown_to_html


class SiteConfig:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = py_yaml.YAMLParser(config_file_path)

    def get_mapping(self):
        return self.config.get_mapping()
    

class HTMLContent:
    def __init__(self, markdown_file_path):
        self.markdown_file_path = markdown_file_path
        self.html_content = py_markdown_to_html.MarkdownToHTML(markdown_file_path).md_to_html()

    def get_html_content(self):
        return self.html_content
    

class Layout:
    def __init__(self, layout_path):
        self.layout_path = layout_path
    
    def get_content(self):
        with open(self.layout_path, 'rb') as l: return l.read().decode('utf-8')

    
class Jekyll:
    def __init__(self, input_folder, output_folder, layout_path, config_file_path):
        self.input_folder = input_folder
        self.output_folder = output_folder 
        self.layout_path = layout_path
        self.config_file_path = config_file_path
        self.generate_site()

    def generate_site(self):
        layout, config = Layout(self.layout_path).get_content, SiteConfig(self.config_file_path).get_mapping()
        for md_file in self.input_folder:
            html_content = HTMLContent(md_file)
            self._generate_html_page(layout, config, html_content)

    def _generate_html_page(self, layout, config, html_content):
        