from ai_systems_design.py_jekyll.py_jekyll import Jekyll 

if __name__ == "__main__":
    jekyll = Jekyll('ai_systems_design/py_jekyll/input', 
                    'ai_systems_design/py_jekyll/output', 
                    'ai_systems_design/py_jekyll/layout.html', 
                    'ai_systems_design/py_jekyll/config.yaml')