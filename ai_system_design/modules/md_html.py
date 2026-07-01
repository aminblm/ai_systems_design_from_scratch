# md_html.py
import re
from enum import Enum 
from pathlib import Path
from typing import Generator, Optional

from ai_system_design.kernel.utils import IOUtility
from ai_system_design.kernel.mixins import LoggableMixin


class MDSpecialCases(Enum):
    BOLD = r'\*\*(.*?)\*\*'
    ITALIC = r'\*(.*?)\*'
    MULTILINE_CODE = r'```(.*?)```'
    INLINE_CODE = r'`(.*?)`'
    LINK = r'\[(.*?)\]\((.*?)\)'
    IMAGE = r'!\[(.*?)\]\((.*?)\)'


class MarkdownParser(LoggableMixin):
    """Handles the transformation of Markdown text strings into structured HTML."""
    
    def __init__(self) -> None:
        super().__init__()
        self.inline_rules = [
            (MDSpecialCases.BOLD.value, r'<strong>\1</strong>'),
            (MDSpecialCases.ITALIC.value, r'<em>\1</em>'),
            (MDSpecialCases.INLINE_CODE.value, r'<code>\1</code>'),
            (MDSpecialCases.LINK.value, r'<a href="\2">\1</a>'),
            (MDSpecialCases.IMAGE.value, r'<img src="\2" alt="\1">'),
        ]
        self.yaml_config: str = ""
        self.logger.info("MarkdownParser initialized.")

    def _parse_inline_elements(self, text: str) -> str:
        """Applies regex conversions for inline specials (bold, italic, links)."""
        for pattern, replacement in self.inline_rules:
            text = re.sub(pattern, replacement, text)
        return text
    
    def _parse_metadata(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to strip front-matter metadata (lines between '---')."""
        for line in lines_iterator:
            if line == '---':
                # Skip everything until the closing metadata tag
                for close_line in lines_iterator:
                    if close_line.strip() == '---':
                        break
                    else:
                        self.yaml_config += close_line + "\n"
                continue
            yield line

    def _parse_multiline_html_tags(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line html tags."""
        for line in lines_iterator:
            if line.strip().startswith("<") and line.strip().endswith('"'): 
                content = line.strip()
                for close_line in lines_iterator:
                    content += " " + close_line.strip()
                    if close_line.startswith("</"):
                        break
                yield "\n" + content + "\n"
                continue
            yield line
    
    def _parse_multiline_code(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line code blocks."""
        for line in lines_iterator:
            if line.startswith("```") and not line.endswith('```'): 
                yield "\n<pre><code>"
                for close_line in lines_iterator:
                    if close_line.startswith("```"):
                        break
                    else:
                        yield "</>" + close_line + "</>"
                yield "</code></pre>\n"
                continue
            yield line
    
    def _parse_raw(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse raw blocks."""
        for line in lines_iterator:
            if line == "{% raw %}": 
                for close_line in lines_iterator:
                    if close_line == "{% endraw %}":
                        break
                    else:
                        if close_line != "{% endraw %}":
                            yield close_line
                continue
            yield line

    def _parse_bullet_points(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line bullet points."""
        for line in lines_iterator:
            if line.startswith("* ") or line.startswith('- '): 
                yield f"\n<ul>"
                yield f"\t<li>{self._parse_inline_elements(line[2:].strip())}</li>"
                for close_line in lines_iterator:
                    if close_line.startswith("* ") or close_line.startswith('- '):
                        yield f"\t<li>{self._parse_inline_elements(close_line[2:].strip())}</li>"
                    else:
                        yield f"</ul>\n"
                        break
                continue
            yield line

    def _parse_ordered_list(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line ordered list."""
        for line in lines_iterator:
            if line.strip() and line.split(maxsplit=1)[0][:-1].isdigit() and line.split(maxsplit=1)[0][-1] == ".": 
                yield f"\n<ol>"
                yield f"\t<li>{self._parse_inline_elements(line[2:].strip())}</li>"
                for close_line in lines_iterator:
                    if close_line and close_line.split(maxsplit=1)[0][:-1].isdigit() and close_line.split(maxsplit=1)[0][-1] == ".":
                        yield f"\t<li>{self._parse_inline_elements(close_line[2:].strip())}</li>"
                    else:
                        yield f"</ol>\n"
                        break
                continue
            yield line

    def _parse_tables(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line tables."""
        for line in lines_iterator:
            if line.startswith("| ") and line.endswith(' |'): 
                yield '\n<table border="1" border-collapse="collapse">'
                yield "\t<thead>"
                yield "\t\t<tr>"
                for table_head in line.split("|")[1: -1]:
                    yield f"\t\t\t<th>{self._parse_inline_elements(table_head.strip())}</th>"
                yield "\t\t</tr>"
                yield "\t</thead>\n"
                yield "\t<tbody>"
                for close_line in lines_iterator:
                    if "--- |" in close_line:
                        continue
                    if close_line.startswith("| ") and close_line.endswith(' |'):
                        yield "\t\t<tr>"
                        for table_body in close_line.split("|")[1: -1]:
                            yield f"\t\t\t<td>{self._parse_inline_elements(table_body.strip())}</td>"
                        yield "\t\t</tr>"
                    else:
                        break
                yield "\t</tbody>"
                yield "</table>\n"
                continue
            yield line

    def parse_line(self, line: str) -> str:
        """Parses block-level elements."""
        if not line: 
            return ""
        
        # Headings
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            content = line.lstrip('#').strip()
            return f"<h{level}>{self._parse_inline_elements(content)}</h{level}>"
        
        # HTML tag
        if line.startswith('<') and line.endswith(">"):
            return f"{line}"

        # Blockquotes
        if line.startswith('>'):
            content = line[1:].strip()
            return f"<blockquote>{self._parse_inline_elements(content)}</blockquote>"

        # Multiline code blocks (Simplistic structural handling)
        if line.startswith('```') and line.endswith('```'):
            content = line.strip('`').strip()
            return f"<pre><code>{self._parse_inline_elements(content)}</code></pre>"
        
        # Multiline HTML Block
        if line.startswith('<') and line.endswith('"'):
            return f"{line}"

        # Default paragraph
        return f"<p>{self._parse_inline_elements(line)}</p>"
    
        #TODO Header wrapped within a link pattern
    
    def to_html(self, markdown_generator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Converts an entire markdown document string into an HTML string."""
        cleaned_lines_generator = self._parse_tables(
            self._parse_bullet_points(
                self._parse_ordered_list(
                    self._parse_multiline_code(
                        self._parse_raw(
                            self._parse_multiline_html_tags(
                                self._parse_metadata(
                                    markdown_generator
                                )
                            )
                        )
                    )
                )
            )
        )
    
        for line in cleaned_lines_generator:
            parsed = self.parse_line(line.strip())
            if parsed:
                yield parsed
        

class MarkdownConverterFacade(LoggableMixin):
    """Clean operational interface for client applications."""

    def __init__(self, parser: MarkdownParser = MarkdownParser()) -> None:
        super().__init__()
        self.parser = parser
        self.logger.info("MarkdownConverterFacade initialized.")

    def get_yaml_config(self) -> str:
        return self.parser.yaml_config
    
    def convert_file(self, input_path: str | Path, output_path: Optional[str | Path] = None) -> Generator[str, None, None]:
        """Reads markdown from file, converts it, and writes out HTML."""
        html_content_generator = self.parser.to_html(IOUtility().text_to_lines_generator(IOUtility().read_decoded(input_path), strip=True))
        if output_path:
            IOUtility().write_encoded(output_path, html_content_generator)
        return html_content_generator

    def convert_text(self, text: str) -> Generator[str, None, None]:
        """Direct string interface."""
        return self.parser.to_html(IOUtility().text_to_lines_generator(text))

    def md_text_to_html_file(self, html_file_path: str | Path, html_content: Generator[str, None, None]): IOUtility().write_encoded(html_file_path, html_content)
    
    def gen_html_from_md_text(self, md_text): return self.parser.to_html(md_text.split("\n"))