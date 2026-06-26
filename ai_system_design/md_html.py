# md_html.py
from enum import Enum 
import re
from typing import Generator
from pathlib import Path

from ai_system_design.utils import IOUtility
from ai_system_design import logger


class MDSpecialCases(Enum):
    BOLD = r'\*\*(.*?)\*\*'
    ITALIC = r'\*(.*?)\*'
    MULTILINE_CODE = r'```(.*?)```'
    INLINE_CODE = r'`(.*?)`'
    LINK = r'\[(.*?)\]\((.*?)\)'
    IMAGE = r'!\[(.*?)\]\((.*?)\)'


class MarkdownParser:
    """Handles the transformation of Markdown text strings into structured HTML."""
    
    def __init__(self) -> None:
        self.inline_rules = [
            (MDSpecialCases.BOLD.value, r'<strong>\1</strong>'),
            (MDSpecialCases.ITALIC.value, r'<em>\1</em>'),
            (MDSpecialCases.INLINE_CODE.value, r'<code>\1</code>'),
            (MDSpecialCases.LINK.value, r'<a href="\2">\1</a>'),
            (MDSpecialCases.IMAGE.value, r'<img src="\2" alt="\1">'),
        ]

    def _parse_inline_elements(self, text: str) -> str:
        """Applies regex conversions for inline specials (bold, italic, links)."""
        for pattern, replacement in self.inline_rules:
            text = re.sub(pattern, replacement, text)
        return text
    
    def _clean_metadata(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to strip front-matter metadata (lines between '---')."""
        for line in lines_iterator:
            if line == '---':
                # Skip everything until the closing metadata tag
                for close_line in lines_iterator:
                    if close_line.strip() == '---':
                        break
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
                yield content
                continue
            yield line
    
    def _parse_multiline_code(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line code blocks."""
        for line in lines_iterator:
            if line.startswith("```") and not line.endswith('```'): 
                content = line.replace(line.split("```")[1], '')
                for close_line in lines_iterator:
                    content += "\n" + close_line
                    if close_line.startswith("```"):
                        break
                yield content
                continue
            yield line

    def _parse_bullet_points(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line bullet points."""
        for line in lines_iterator:
            if line.startswith("* ") or line.startswith('- '): 
                content = f"<ul>\n\t<li>{self._parse_inline_elements(line[2:].strip())}</li>"
                for close_line in lines_iterator:
                    if close_line.startswith("* ") or close_line.startswith('- '):
                        content += f"\n\t<li>{self._parse_inline_elements(close_line[2:].strip())}</li>"
                    else:
                        content += f"\n</ul>"
                        break
                yield content
                continue
            yield line

    def _parse_tables(self, lines_iterator: Generator[str, None, None]) -> Generator[str, None, None]:
        """Generator to parse multi-line tables."""
        for line in lines_iterator:
            if line.startswith("| ") and line.endswith(' |'): 
                content = '<table border="1" border-collapse="collapse">\n\t<thead>\n\t\t<tr>\n'
                for table_head in line.split("|")[1: -1]:
                    content += f"\t\t\t<th>{self._parse_inline_elements(table_head.strip())}</th>\n"
                content += "\t\t</tr>\n\t</thead>\n\t<tbody>\n"
                for close_line in lines_iterator:
                    if "--- |" in close_line:
                        continue
                    if close_line.startswith("| ") and close_line.endswith(' |'):
                        content += "\t\t<tr>\n"
                        for table_body in close_line.split("|")[1: -1]:
                            content += f"\t\t\t<td>{self._parse_inline_elements(table_body.strip())}</td>\n"
                        content += "\t\t</tr>\n"
                    else:
                        break
                content += "\t</tbody>\n</table>\n"
                yield content
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
    
    def to_html(self, markdown_text: str) -> Generator[str, None, None]:
        """Converts an entire markdown document string into an HTML string."""
        cleaned_lines_iterator = self._parse_tables(
            self._parse_bullet_points(
                self._parse_multiline_code(
                    self._parse_multiline_html_tags(
                        self._clean_metadata(
                            IOUtility.text_to_lines_iterator(markdown_text)
                        )
                    )
                )
            )
        )
    
        for line in cleaned_lines_iterator:
            parsed = self.parse_line(line.strip())
            if parsed:
                yield parsed

class MarkdownConverterFacade:
    """Clean operational interface for client applications."""

    def __init__(self, parser: MarkdownParser = MarkdownParser()) -> None:
        self.parser = parser

    def convert_file(self, input_path: str | Path, output_path: str | Path = None) -> str:
        """Reads markdown from file, converts it, and writes out HTML."""
        html_content = self.parser.to_html(IOUtility.read_decoded(input_path))
        if output_path:
            IOUtility.write_encoded(output_path, html_content)
        return html_content

    def convert_text(self, text: str) -> str:
        """Direct string interface."""
        return self.parser.to_html(text)

    def md_text_to_html_file(self, html_file_path: str | Path, html_content: str): IOUtility.write_encoded(html_file_path, html_content)

    def gen_html_from_md_file(self, markdown_file_path: str | Path): return self.parser.to_html(IOUtility.read_decoded(markdown_file_path))
    
    def gen_html_from_md_text(self, md_text): return self.parser.to_html(md_text.split("\n"))