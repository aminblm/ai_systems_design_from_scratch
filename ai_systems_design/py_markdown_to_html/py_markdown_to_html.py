from enum import Enum 

from ai_systems_design.utils import FileOperationsUtility

class MD_SPECIAL_CASES(Enum):
    BOLD = '**'
    ITALIC = '*'
    MULTILINE_CODE = '```'
    INLINE_CODE = '`'
    LINK = '[]()'
    IMAGE = '![]()'


class FileOperations:
    @staticmethod
    def read_markdown_file(markdown_file_path): return FileOperationsUtility.read_decoded(markdown_file_path)

    @staticmethod
    def write_html_file(html_file_path, content): return FileOperationsUtility.write_encoded(html_file_path, content)


class Helpers:
    @staticmethod
    def _ignore_metadata_line(lines):
        # TODO process metadata into dynamic variables
        for i, line in enumerate(lines):
            if line.startswith('---'): return lines[i+1:]
        return lines

    @staticmethod         
    def _is_pure_text(text):
        return not any(special.value in text for special in MD_SPECIAL_CASES)
    

class MarkdownParser:
    @staticmethod
    def _parse_header(line):
        return f"<h{ len(line.split(' ')[0])}>{ " ".join(line.split(' ')[1:]) }</h{ len(line.split(' ')[0]) }"

    @staticmethod
    def _parse_html(line):
        # TODO add support for multiline html
        return line

    @staticmethod
    def _parse_bullet_point(line):
        return f'<li>{ MarkdownParser._parse_markdown_specials(" ".join(line.split(' ')[1:])) }</li>'

    @staticmethod
    def _parse_quote(line):
        return f"<blockquote>{ MarkdownParser._parse_markdown_specials(' '.join(line.split(' ')[1:])) }</blockquote>"

    @staticmethod
    def _parse_multi_line_code(line):
        # TODO support multi-line code
        return f'<pre><code>{ line.split(MD_SPECIAL_CASES.MULTILINE_CODE.value)[1] }</code></pre>'

    @staticmethod
    def _parse_inline_code(line):
        # TODO support multi-line code
        return f'<pre><code>{ line.split(MD_SPECIAL_CASES.INLINE_CODE.value)[1] }</code></pre>'
    
    @staticmethod
    def _parse_bold_html_element(bold_split_element):
        return f'<strong>{ bold_split_element }</strong>'
    
    @staticmethod
    def _parse_italic_html_element(italic_split_element):
        return f"<em>{ italic_split_element }</em>"

    @staticmethod
    def _parse_pure_text_line(line):
        return f'<p>{ line }</p>'
    
    @staticmethod
    def _parse_markdown_specials(markdown_content):
        # TODO markdwn proper specials nesting
        html_content = ""
        if len(markdown_content.split(MD_SPECIAL_CASES.BOLD.value)) % 2 != 0:
            html_content += MarkdownParser._parse_text_with_possible_bold(markdown_content)
        elif len(markdown_content.split(MD_SPECIAL_CASES.ITALIC.value)) % 2 != 0:
            html_content += MarkdownParser._parse_text_with_possible_italic(markdown_content)
        return html_content
    
    @staticmethod
    def _parse_text_with_possible_italic(markdown_content):
        # TODO markdwn proper specials nesting
        html_content = ""
        italic_split = markdown_content.split(MD_SPECIAL_CASES.ITALIC.value)
        for i, italic_split_element in enumerate(italic_split):
            if italic_split[0].startswith(MD_SPECIAL_CASES.ITALIC.value):
                if i%2 == 0: html_content += MarkdownParser._parse_italic_html_element(italic_split_element)
                else: html_content += italic_split_element
            else:
                if i%2 == 1: html_content += MarkdownParser._parse_italic_html_element(italic_split_element)
                else: html_content += italic_split_element
        return html_content
    
    @staticmethod
    def _parse_text_with_possible_bold(markdown_content):
        # TODO markdwn proper specials nesting
        html_content = ""
        bold_split = markdown_content.split(MD_SPECIAL_CASES.BOLD.value)
        if bold_split[0].startswith(MD_SPECIAL_CASES.BOLD.value):
            for i, bold_split_element in enumerate(bold_split):
                if i%2 == 0: html_content += MarkdownParser._parse_bold_html_element(bold_split_element)
                else: html_content += MarkdownParser._parse_text_with_possible_italic(bold_split_element)
        else:
            for i, bold_split_element in enumerate(bold_split): 
                if i%2 == 1: html_content += MarkdownParser._parse_bold_html_element(bold_split_element)
                else: html_content += MarkdownParser._parse_text_with_possible_italic(bold_split_element)
        return html_content
    
    @staticmethod
    def _parse_line(line):
        line = line.strip()
        if line.startswith('#'): return MarkdownParser._parse_header(line)
        elif line.startswith('---'): return '<br>'
        elif line.startswith("<"): return MarkdownParser._parse_html(line)
        elif line.startswith(">"): return MarkdownParser._parse_quote(line)
        elif line.startswith("* ") or line.startswith("- "): return MarkdownParser._parse_bullet_point(line)
        elif line.startswith(MD_SPECIAL_CASES.MULTILINE_CODE.value): return MarkdownParser._parse_multi_line_code(line)
        elif line.startswith(MD_SPECIAL_CASES.INLINE_CODE.value): return MarkdownParser._parse_inline_code(line)
        elif line.endswith('"') or line.endswith('">'): return '' #TODO Multi-line HTML
        elif line.startswith('[') or line.startswith('!'): return '' #TODO Links and images
        elif Helpers._is_pure_text(line): return MarkdownParser._parse_pure_text_line(line)
        else: return MarkdownParser._parse_markdown_specials(line)

    @staticmethod
    def parse(lines):
        html = ''
        if lines[0].startswith('---'): lines = Helpers._ignore_metadata_line(lines[1:])
        for line in lines: html += f'{ MarkdownParser._parse_line(line) }\n'
        return html


class MarkdownToHTMLBuilder:
    def __init__(self):
        self.markdown_file_path = ""
        self.markdown_text = ""

    def set_markdown_file_path(self, markdown_file_path):
        self.markdown_file_path = markdown_file_path
        return self

    def set_markdown_text(self, markdown_text):
        self.markdown_text = markdown_text
        return self

    def build(self):
        return MarkdownToHTML(
            markdown_file_path = self.markdown_file_path,
            markdown_text = self.markdown_text,
        )
    
    @staticmethod
    def create_default(): return MarkdownToHTMLBuilder().build()
    
    @staticmethod
    def create_from_file(path): return MarkdownToHTMLBuilder().set_markdown_file_path(path).build()
    
    @staticmethod
    def create_from_text(text): return MarkdownToHTMLBuilder().set_markdown_text(text).build()
    

class MarkdownToHTML:
    def __init__(self, markdown_file_path=None, markdown_text=None):
        self.markdown_file_path, self.markdown_text = markdown_file_path, markdown_text

    def md_file_to_html(self): return HTMLGenerator.gen_html_from_md_file(self.markdown_file_path)
    
    def md_text_to_html(self): return HTMLGenerator.gen_html_from_md_text(self.markdown_text)
    

class HTMLGenerator: 
    @staticmethod
    def md_text_to_html_file(html_file_path, html_content): FileOperations.write_html_file(html_file_path, html_content)

    @staticmethod
    def gen_html_from_md_file(markdown_file_path): return MarkdownParser.parse(FileOperations.read_markdown_file(markdown_file_path).split("\n"))
    
    @staticmethod
    def gen_html_from_md_text(md_text): return MarkdownParser.parse(md_text.split("\n"))