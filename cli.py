# cli.py

"""Global CLI entry point."""

from ai_system_design.cli import doc_engine_cli, site_generator_cli


if __name__ == "__main__":
    #ISSUE #2 pasring cli module arguments needs to be done i.e. python cli.py -m doc_engine_cli --source SOURCE --output-path OUTPUT_PATH [--secondary-output-path SECONDARY_OUTPUT_PATH]
    # doc_engine_cli()
    
    site_generator_cli()