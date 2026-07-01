# cli.py
"""
Main CLI Controller for the AI System Design CLI Modules. 
"""

def doc_engine_cli():
    from ai_system_design.kernel.doc_engine import DocEngineCLI
    DocEngineCLI().cli()

def site_generator_cli():
    from ai_system_design.modules.site_generator.site_generator import GenerateSiteCLI
    GenerateSiteCLI().cli()