import os

from ai_systems_design.py_yaml import YAMLParser
from ai_systems_design.py_markdown_to_html.py_markdown_to_html import MarkdownToHTML

class LayoutHandler:
    @staticmethod
    def get_layout(layout_path):
        with open(layout_path, 'rb') as l: return l.read().decode('utf-8')


class ConfigHandler:
    @staticmethod
    def get_config_mapping(config_file_path):
        return YAMLParser(config_file_path).get_mapping()


class HTMLRenderer:
    @staticmethod
    def render_html(layout, config, md_file_path):
        html, config['content'] = layout, MarkdownToHTML(md_file_path).md_to_html()
        for key in config: html = html.replace('{{ site.' + key + ' }}', config[key])
        return html
    

class HTMLGenerator:
    @staticmethod
    def generate_html_page(layout, config, md_file_path, html_file_path):
        html = HTMLRenderer.render_html(layout, config, md_file_path)
        with open(html_file_path, 'wb') as html: html.write(layout.encode('utf-8'))

    @staticmethod
    def generate_html_pages(input_folder, output_folder, layout, config):
        for md_file_name in os.listdir(input_folder):
            md_file_path, html_file_path = DependenciesManager.get_files_paths(md_file_name, input_folder, output_folder)
            if os.path.isfile(md_file_path): HTMLGenerator.generate_html_page(layout, config, md_file_path, html_file_path)


class DependenciesManager:
    @staticmethod
    def get_dependencies(layout_path, config_file_path):
        return LayoutHandler.get_layout(layout_path), ConfigHandler.get_config_mapping(config_file_path)

    @staticmethod
    def get_files_paths(md_file_name, input_folder, output_folder):
        html_file_name = f"{ md_file_name.split('.md')[0] }.html"
        return tuple(map(lambda x, y: os.path.join(x, y), (input_folder, output_folder), (md_file_name, html_file_name)))
    

class Jekyll:
    def __init__(self, input_folder, output_folder, layout_path, config_file_path):
        self.input_folder, self.output_folder = input_folder, output_folder 
        self.layout, self.config = DependenciesManager.get_dependencies(layout_path, config_file_path)

    def generate_site(self):
        HTMLGenerator.generate_html_pages(self.input_folder, self.output_folder, self.layout, self.config)