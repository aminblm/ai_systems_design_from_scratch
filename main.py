from ai_systems_design.py_jekyll.py_jekyll import Jekyll 
from ai_systems_design.py_slug_generator import SlugGenerator, TerminalInterface

def generate_jekyll_site():
    jekyll = Jekyll('ai_systems_design/py_jekyll/input', 
                    'ai_systems_design/py_jekyll/output', 
                    'ai_systems_design/py_jekyll/layout.html', 
                    'ai_systems_design/py_jekyll/config.yaml')

def generate_slugs():
    slug_engine = SlugGenerator()
    interface = TerminalInterface(generator=slug_engine)
    interface.run()

if __name__ == "__main__":
    generate_jekyll_site()