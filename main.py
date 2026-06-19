from ai_systems_design.site_generator.site_generator import SiteGenerator 
from ai_systems_design.py_slug_generator import SlugGenerator, TerminalInterface

def generate_site():
    base_path = 'ai_systems_design/site_generator/'
    SiteGenerator(f'{base_path}layout.html', f'{base_path}config.yaml').generate_site(f'{base_path}input')

def generate_slugs():
    slug_engine = SlugGenerator()
    interface = TerminalInterface(generator=slug_engine)
    interface.run()

if __name__ == "__main__":
    generate_site()
    #generate_slugs()