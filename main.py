from ai_systems_design.py_jekyll.py_jekyll import Jekyll 
from ai_systems_design.py_slug_generator import SlugGenerator, TerminalInterface

def generate_jekyll_site():
    base_path = 'ai_systems_design/py_jekyll/'
    Jekyll.generate_site(f'{base_path}input', f'{base_path}layout.html', f'{base_path}config.yaml')

def generate_slugs():
    slug_engine = SlugGenerator()
    interface = TerminalInterface(generator=slug_engine)
    interface.run()

if __name__ == "__main__":
    #generate_jekyll_site()
    generate_slugs()