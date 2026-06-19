import os, logging, traceback

from ai_systems_design.py_yaml import YAMLParser
from ai_systems_design.py_markdown_to_html.py_markdown_to_html import MarkdownToHTMLBuilder


class ErrorHandler:
    @staticmethod
    def with_error_handling(func):
        def wrapper(*args, **kwargs):
            if 'input_dir' in kwargs and not os.path.isdir(kwargs['input_dir']):
                raise ValueError(f"Input dir {kwargs['input_dir'] } is not a dir.")
            try: result = func(*args, **kwargs); return result
            except Exception as e: 
                logging.error(f"Error in {func.__name__}: {e}"); 
                logging.error(traceback.format_exc()); return None
        return wrapper
    

class FileOperations:
    @staticmethod
    def get_file_paths(md_file_name, input_dir, output_dir):
        html_file_name = f"{ md_file_name.split('.md')[0] }.html"
        return tuple(map(lambda x, y: os.path.join(x, y), (input_dir, output_dir), (md_file_name, html_file_name)))
  
    @staticmethod
    @ErrorHandler.with_error_handling
    def create_output_dir(input_dir):
        output_dir = os.path.join(os.path.dirname(input_dir), 'output')
        if not os.path.exists(output_dir): os.makedirs(output_dir, exist_ok=True)
        return output_dir


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
        html = layout.replace('{{ site.content }}', MarkdownToHTMLBuilder.create_from_file(md_file_path).md_file_to_html())
        for key in config: html = html.replace('{{ site.' + key + ' }}', config[key])
        return html
    

class HTMLGenerator:
    @staticmethod
    @ErrorHandler.with_error_handling
    def generate_html_page(layout, config, md_file_path, html_file_path):
        with open(html_file_path, 'wb') as html: html.write(HTMLRenderer.render_html(layout, config, md_file_path).encode('utf-8'))

    @staticmethod
    @ErrorHandler.with_error_handling
    def generate_html_pages(input_dir, output_dir, layout, config):
        for md_file_name in os.listdir(input_dir):
            md_file_path, html_file_path = FileOperations.get_file_paths(md_file_name, input_dir, output_dir)
            if os.path.isfile(md_file_path): HTMLGenerator.generate_html_page(layout, config, md_file_path, html_file_path)


class DependenciesManager:
    @staticmethod
    def get_dependencies(input_dir, layout_path, config_file_path):
        return input_dir, FileOperations.create_output_dir(input_dir), LayoutHandler.get_layout(layout_path), ConfigHandler.get_config_mapping(config_file_path)


class Jekyll:
    @staticmethod
    def generate_site(input_dir, layout_path, config_file_path):
        HTMLGenerator.generate_html_pages(*DependenciesManager.get_dependencies(input_dir, layout_path, config_file_path))