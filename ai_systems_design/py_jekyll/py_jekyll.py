"""
about:
    - title: py_jekyll.py
    - author: Amin Boulouma
    - description: Takes a folder of Markdown files and converts them into an output folder of HTML files following a layout and a yaml configuration.

i/o:
    - input: input folder path, output folder path, layout file path, config file path
    - output: html files into the output folder

features:
    - generates a site of html files from markdown files
    - dynamic variable

implementations details:
    - order preservation
    - element recognition
    - nested elements

limitations:
    - dynamic variables
    - advanced site generation

examples: 
    - you can see examples in the input / output folder within this folder
"""

import os

from ai_systems_design.py_yaml import YAMLParser
from ai_systems_design.py_markdown_to_html.py_markdown_to_html import MarkdownToHTML


class SiteConfig:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = YAMLParser(config_file_path)

    def get_mapping(self):
        return self.config.get_mapping()
    

class HTMLContent:
    def __init__(self, markdown_file_path):
        self.markdown_file_path = markdown_file_path
        self.html_content = MarkdownToHTML(markdown_file_path).md_to_html()

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
        layout, config = Layout(self.layout_path).get_content(), SiteConfig(self.config_file_path).get_mapping()
        for md_file in os.listdir(self.input_folder):
            md_file_path = os.path.join(self.input_folder, md_file)
            html_file_path = os.path.join(self.output_folder, f"{ md_file.split('.md')[0] }.html")
            html_content = HTMLContent(md_file_path).get_html_content()
            if os.path.isfile(md_file_path): self._generate_html_page(layout, config, html_content, html_file_path)
        print("Site generated.")

    def _generate_html_page(self, layout, config, html_content, html_file_path):
        layout = layout.replace('{{ site.title }}', config['title'])
        layout = layout.replace('{{ site.description }}', config['description'])
        layout = layout.replace('{{ site.css }}', config['css'])
        layout = layout.replace('{{ content }}', html_content)
        layout = layout.replace('{{ site.footer_text }}', config['footer_text'])
        layout = layout.replace('{{ site.url }}', config['url'])
        layout = layout.replace('{{ site.author }}', config['author'])
        with open(html_file_path, 'wb') as html: html.write(layout.encode('utf-8'))
