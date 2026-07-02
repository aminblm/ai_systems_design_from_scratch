# site_generator.py

"""Generate HTML website from markdown files directory."""

import traceback
from pathlib import Path
from typing import Dict, Tuple, Generator

from ai_system_design.modules.safe_yaml_parser import ConfigurationBuilder
from ai_system_design.modules.md_html import MarkdownConverterFacade
from ai_system_design.kernel.utils import IOUtility

from ai_system_design.kernel.mixins import LoggableMixin, CLIMixin


class GenerateSiteCLI(CLIMixin):
    """GenerateSiteCLI Class."""

    def __init__(self) -> None:
        """GenerateSiteCLI `__init__(self) -> None` Constructor."""
        super().__init__()
        self.parser.add_argument("--input-directory", required=True)
        self.parser.add_argument("--layout", required=False)
        self.parser.add_argument("--config", required=False)
        self.logger.info("GenerateSiteCLI initialized.")
    
    def cli(self):
        """Usage: `cli.py [-h] --input-directory INPUT_DIRECTORY [--layout LAYOUT] [--config CONFIG]`"""
        super().cli()
        args = self.parser.parse_args()
        BASE_PATH = 'ai_system_design/modules/site_generator/'
        DEFAULT_LAYOUT = f'{BASE_PATH}layout.html'
        DEFAULT_CONFIG = f'{BASE_PATH}config.yaml'
        if not args.layout and not args.config:
            SiteGenerator(DEFAULT_LAYOUT, DEFAULT_CONFIG).generate_site(args.input_directory)
        elif not args.layout and args.config:
            SiteGenerator(args.layout, DEFAULT_CONFIG).generate_site(args.input_directory)
        elif args.layout and not args.config:
            SiteGenerator(DEFAULT_LAYOUT, args.config).generate_site(args.input_directory)
        else:
            SiteGenerator(args.layout, args.config).generate_site(args.input_directory)


class SiteGenerator(LoggableMixin):
    """Coordinater class to orchestrate the Markdown to Template-bound HTML building process"""

    def __init__(self, layout_path: str | Path, config_file_path: str | Path) -> None:
        """SiteGenerator `__init__(self, layout_path: str | Path, config_file_path: str | Path) -> None` Constructor."""
        super().__init__()
        self.layout_path = Path(layout_path)
        self.config_file_path = Path(config_file_path)
        self.logger.info("SiteGenerator initialized.")

        # Load assets during initialization rather than on every loop iteration
        self.layout_template = self._load_layout()
        self.config_mappings = self._load_config()

    #TODO
    # Possible copy of the styles file to the output folder for dynamic styling
    def _copy_styles(self) -> None:
        """SiteGenerator `_copy_styles(self) -> None` private method."""
        return None
    
    def _load_layout(self) -> str:
        """SiteGenerator `_load_layout(self) -> str` private method."""
        return IOUtility().read_decoded(self.layout_path)
    
    def _load_config(self) -> Dict[str, str]:
        """SiteGenerator ` _load_config(self) -> Dict[str, str]` private method."""
        return ConfigurationBuilder().from_file(self.config_file_path).build().to_dict()
    
    def _get_header_lines(self, html_generator: Generator[str, None, None]) -> Generator[str, None, None]:
        """SiteGenerator ` _get_header_lines(self, html_generator: Generator[str, None, None]) -> Generator[str, None, None]` private method."""
        for line in html_generator:
            if line.strip() == "<head>":
                for closed_line in html_generator:
                    if closed_line.strip() == "</head>":
                        break 
                    else:
                        yield closed_line.strip()

    def _clean_header_lines(self, html_generator: Generator[str, None, None]) -> Generator[str, None, None]:
        """SiteGenerator `_clean_header_lines(self, html_generator: Generator[str, None, None]) -> Generator[str, None, None]` private method."""
        for line in html_generator:
            if line.strip() == "<head>":
                for closed_line in html_generator:
                    if closed_line.strip() == "</head>":
                        break 
                    continue
            yield line

    def _render_html(self, md_file_path: Path) -> str:
        """Injects compiled markdown content and config mappings into the layout"""

        markdown_file_converter = MarkdownConverterFacade()

        # Hydrate head content
        html = self.layout_template.replace('{{ head.content }}', "\n\t\t".join(self._get_header_lines(markdown_file_converter.convert_file(md_file_path))))

        # Hydrate primary content block
        html = html.replace('{{ site.content }}', "\n\t\t\t\t".join(self._clean_header_lines(markdown_file_converter.convert_file(md_file_path))))

        # Hydrate,etadata key/value template tokens
        for key, value in self.config_mappings.items():
            html = html.replace(f'{{{{ site.{key} }}}}', str(value))
            html = html.replace(f'{{{{ page.{key} | default: site.{key} }}}}', str(value))

        # Load Markdown Page Config
        markdown_config_mappings = ConfigurationBuilder().from_text(markdown_file_converter.get_yaml_config()).build().to_dict()
        
        # Hydrate,etadata key/value template tokens in individual files
        for key, value in markdown_config_mappings.items():
            html = html.replace(f'{{{{ page.{key} }}}}', str(value))
            html = html.replace(f'{{{{ page.{key} | default: site.{key} }}}}', str(value))

        return html
    
    def _resolve_paths(self, md_file: Path, input_dir: Path, output_dir: Path) -> Tuple[Path, Path]:
        """Calculates input and output targets safely using modern path objects."""
        # Handles complex names cleanly (e.g. "my.post.md" -> "my.post.html")
        html_filename = f"{md_file.stem}.html"
        return md_file, output_dir / html_filename
    
    def generate_site(self, input_directory: str | Path) -> None:
        """Processes all Markdown files within the targeted input directory."""
        input_dir = Path(input_directory)

        if not input_dir.is_dir():
            raise ValueError(f'Target input path is not a valid directory: {input_dir}')

        # Automatically establish output directory as a sibling to input
        output_dir = input_dir.parent / 'sg_output'
        output_dir.mkdir(parents=True, exist_ok=True)

        # Batch process directory contents safely
        for file_path in input_dir.iterdir():
            if not file_path.is_file() or file_path.suffix.lower() != '.md':
                continue

            try:
                src_path, dest_path = self._resolve_paths(file_path, input_dir, output_dir)
                rendered_content = self._render_html(src_path)

                IOUtility().write_encoded(dest_path, IOUtility().text_to_lines_generator(rendered_content, strip=False))
                self.logger.info(f"Successfully generate page: {dest_path.name}")

            except Exception as err:
                self.logger.error(f" Failed processing {file_path.name}: {err}")
                self.logger.debug(traceback.format_exc())
