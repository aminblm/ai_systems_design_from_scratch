#TODO Implement CLI Interface per module with CLIMixin

def doc_engine_cli():
    from ai_system_design.kernel.doc_engine import DocEngineCLI
    DocEngineCLI().cli()