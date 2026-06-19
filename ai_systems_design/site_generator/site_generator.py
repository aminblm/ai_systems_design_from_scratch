import os, logging, traceback
from pathlib import Path
from typing import Dict, Union, Tuple 

from ai_systems_design.py_yaml import YAMLBuilder
from ai_systems_design.md_html import MarkdownConverterFacade
from ai_systems_design.utils import FileOperationsUtility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SiteGenerator:
    """Coordinater class to orchestrate the MArkdown to Template-bound HTML building process"""

    def __init__(self, layout_path: Union[str, Path], config_file_path: Union[str, Path]) -> None:
        self.layout_path = Path(layout_path)
        self.config_file_path = Path(config_file_path)

        # Load assets during initialization rather than on every loop iteration
        self.layout_template = self._load_layout()
        self.config_mappings = self._load_config()

    def _load_layout(self) -> str:
        return FileOperationsUtility.read_decoded(str(self.layout_path))
    
    def _load_config(self) -> Dict[str, str]:
        return YAMLBuilder.create_from_file(str(self.config_file_path)).get_mapping_from_file()
    
    def _render_html(self, md_file_path: Path) -> str:
        """Injects compiled markdown content and config mappings into the layout"""
        md_html_content = MarkdownConverterFacade().convert_file(str(md_file_path))

        # Hydrate primary content block
        html = self.layout_template.replace('{{ site.content }}', md_html_content)

        # Hydrate ,etadata key/value template tokens
        for key, value in self.config_mappings.items():
            html = html.replace(f'{{{{ site.{key} }}}}', str(value))
        return html
    
    def _resolve_paths(self, md_file: Path, input_dir: Path, output_dir: Path) -> Tuple[Path, Path]:
        """Calculates input and output targets safely using modern path objects."""
        # Handles complex names cleanly (e.g. "my.post.md" -> "my.post.html")
        html_filename = f"{md_file.stem}.html"
        return md_file, output_dir / html_filename
    
    def generate_site(self, input_directory: Union[str, Path]) -> None:
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

                FileOperationsUtility.write_encoded(str(dest_path), rendered_content)
                logger.info(f" Successfully generate page: {dest_path.name}")

            except Exception as err:
                logger.error(f" Failed processing {file_path.name}: {err}")
                logger.debug(traceback.format_exc())
