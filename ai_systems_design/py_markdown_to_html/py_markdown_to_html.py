from enum import Enum 
import re
from typing import List, Generator
from ai_systems_design.utils import FileOperationsUtility


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
    
    def _clean_metadata(self, lines: List[str]) -> Generator[str, None, None]:
        """Generator to strip front-matter metadata (lines between '---')."""
        iterator = iter(lines)
        for line in iterator:
            cleaned = line.strip()
            if cleaned == '---':
                # Skip everything until the closing metadata tag
                for close_line in iterator:
                    if close_line.strip() == '---':
                        break
                continue
            yield cleaned

    def parse_line(self, line: str) -> str:
        """Parses block-level elements."""
        if not line: 
            return ""
        
        # Headings
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            content = line.lstrip('#').strip()
            return f"<h{level}>{self._parse_inline_elements(content)}</h{level}>"

        # Blockquotes
        if line.startswith('>'):
            content = line[1:].strip()
            return f"<blockquote>{self._parse_inline_elements(content)}</blockquote>"

        # Bullet points
        if line.startswith(('* ', '- ')):
            content = line[2:].strip()
            return f"<li>{self._parse_inline_elements(content)}</li>"

        # Multiline code blocks (Simplistic structural handling)
        if line.startswith('```'):
            content = line.strip('`').strip()
            return f"<pre><code>{self._parse_inline_elements(content)}</code></pre>"

        # Default paragraph
        return f"<p>{self._parse_inline_elements(line)}</p>"
    

    def to_html(self, markdown_text: str) -> str:
        """Converts an entire markdown document string into an HTML string."""
        raw_lines = markdown_text.splitlines()
        cleaned_lines = self._clean_metadata(raw_lines)

        html_blocks = []
        for line in cleaned_lines:
            parsed = self.parse_line(line)
            if parsed:
                html_blocks.append(parsed)

        return "\n".join(html_blocks)
    

class MarkdownConverterFacade:
    """Clean operational interface for client applications."""

    def __init__(self, parser: MarkdownParser = None) -> None:
        self.parser = parser or MarkdownParser()

    def convert_file(self, input_path:str, output_path: str = None) -> str:
        """Reads markdown from file, converts it, and writes out HTML."""
        markdown_content = FileOperationsUtility.read_decoded(input_path)
        html_content = self.parser.to_html(markdown_content)
        if output_path:
            FileOperationsUtility.write_encoded(output_path, html_content)
        return html_content

    def convert_text(self, text: str) -> str:
        """Direct string interface."""
        return self.parser.to_html(text)

    @staticmethod
    def md_text_to_html_file(html_file_path, html_content): FileOperations.write_html_file(html_file_path, html_content)

    @staticmethod
    def gen_html_from_md_file(markdown_file_path): return MarkdownParser.parse(FileOperations.read_markdown_file(markdown_file_path).split("\n"))
    
    @staticmethod
    def gen_html_from_md_text(md_text): return MarkdownParser.parse(md_text.split("\n"))