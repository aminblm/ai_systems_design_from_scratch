# cli.py
"""
Main CLI Controller for the AI System Design CLI Modules. 
"""

from typing import Final

def doc_engine():
    from ai_system_design.kernel.doc_engine import DocEngineCLI
    DocEngineCLI().cli()

def site_generator():
    from ai_system_design.modules.site_generator.site_generator import GenerateSiteCLI
    GenerateSiteCLI().cli()

def cli():
    arg: str = "#TODO wainting for nested CLI args parsing."

    match arg:
        case "doc_engine": doc_engine()
        case "site_generator": site_generator()
        case _: print(f"Enter a valid CLI command.")