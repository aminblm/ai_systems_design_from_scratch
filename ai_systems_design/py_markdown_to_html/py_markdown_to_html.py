class MarkdownToHTML:
    def __init__(self, markdown_file_path=None, markdown_text=None, html_file_path=None):
        self.markdown_file_path = markdown_file_path or ""
        self.MD_SPECIALS = {
            'BOLD': '**',
            'ITALIC': '*',
            'MULTILINE_CODE': '```',
            'INLINE_CODE': '`',
            'LINK': '[]()',
            'IMAGE': '![]()'
        }
        self.html_file_path = html_file_path if html_file_path else f'{ self.markdown_file_path.split('.')[0] }.html'
        self.markdown_text = self._read_markdown_file() if not markdown_text else markdown_text
        self._parse_markdown()
        self.html = '\n'.join(self.html_lines)

    def _read_markdown_file(self):
        with open(self.markdown_file_path, 'rb') as md:
            return md.read().decode('utf-8')

    def _parse_markdown(self):
        self.html_lines = []
        lines = self._read_markdown_file().split("\n") if self.markdown_file_path != '' else self.markdown_text.split("\n")
        if lines[0].startswith('---'): lines = self._ignore_metadata_line(lines[1:])
        for line in lines:
            line = line.strip()
            if line.startswith('#'): self._parse_header(line)
            elif line.startswith('---'): self.html_lines.append('<br>')
            elif line.startswith("<"): self._parse_html(line)
            elif line.startswith(">"): self._parse_quote(line)
            elif line.endswith('"') or line.endswith('">'): continue #TODO Multi-line HTML
            elif line.startswith('[') or line.startswith('!'): continue #TODO Links and images
            elif line.startswith("* ") or line.startswith("- "): self._parse_bullet_point(line)
            elif line.startswith(self.MD_SPECIALS['MULTILINE_CODE']): self._parse_multi_line_code(line)
            elif line.startswith(self.MD_SPECIALS['INLINE_CODE']): self._parse_inline_code(line)
            elif self._is_pure_text(line): self._parse_pure_text_line(line)
            else: self.html_lines.append(self._parse_markdown_specials(line))

    def _ignore_metadata_line(self, lines):
        # TODO process metadata into dynamic variables
        for i, line in enumerate(lines):
            if line.startswith('---'): return lines[i+1:]
        return lines
                            
    def _parse_markdown_specials(self, markdown_content):
        html_content = ""
        if len(markdown_content.split(self.MD_SPECIALS['BOLD'])) % 2 != 0:
            html_content += self._append_text_with_possible_bold(markdown_content)
        elif len(markdown_content.split(self.MD_SPECIALS['ITALIC'])) % 2 != 0:
            html_content += self._append_text_with_possible_italic(markdown_content)
        return html_content
    
    def _append_text_with_possible_italic(self, markdown_content):
        html_content = ""
        italic_split = markdown_content.split(self.MD_SPECIALS['ITALIC'])
        for i, italic_split_element in enumerate(italic_split):
            if italic_split[0].startswith(self.MD_SPECIALS['ITALIC']):
                if i%2 == 0: html_content += self._append_italic_html_element(italic_split_element)
                else: html_content += italic_split_element
            else:
                if i%2 == 1: html_content += self._append_italic_html_element(italic_split_element)
                else: html_content += italic_split_element
        return html_content
    
    def _append_text_with_possible_bold(self, markdown_content):
        html_content = ""
        bold_split = markdown_content.split(self.MD_SPECIALS['BOLD'])
        if bold_split[0].startswith(self.MD_SPECIALS['BOLD']):
            for i, bold_split_element in enumerate(bold_split):
                if i%2 == 0: html_content += self._append_bold_html_element(bold_split_element)
                else: html_content += self._append_text_with_possible_italic(bold_split_element)
        else:
            for i, bold_split_element in enumerate(bold_split): 
                if i%2 == 1: html_content += self._append_bold_html_element(bold_split_element)
                else: html_content += self._append_text_with_possible_italic(bold_split_element)
        return html_content
        
    def _append_bold_html_element(self, bold_split_element):
        return f'<strong>{ self._append_text_with_possible_italic(bold_split_element) }</strong>'
    
    def _append_italic_html_element(self, italic_split_element):
        return f"<em>{ italic_split_element }</em>"

    def _parse_header(self, line):
        self.html_lines.append(f"<h{ len(line.split(' ')[0])}>{ " ".join(line.split(' ')[1:]) }</h{ len(line.split(' ')[0]) }")

    def _parse_html(self, line):
        # TODO add support for multiline html
        self.html_lines.append(line)

    def _parse_bullet_point(self, line):
        self.html_lines.append(f'<li>{ self._parse_markdown_specials(" ".join(line.split(' ')[1:])) }</li>')

    def _parse_quote(self, line):
        self.html_lines.append(f"<blockquote>{ self._parse_markdown_specials(' '.join(line.split(' ')[1:])) }</blockquote>")

    def _parse_multi_line_code(self, line):
        # TODO support multi-line code
        self.html_lines.append(f'<pre><code>{ line.split(self.MD_SPECIALS['MULTILINE_CODE'])[1] }</code></pre>')

    def _parse_inline_code(self, line):
        # TODO support multi-line code
        self.html_lines.append(f'<pre><code>{ line.split(self.MD_SPECIALS['INLINE_CODE'])[1] }</code></pre>')

    def _is_pure_text(self, text):
        return not any(special in text for special in self.MD_SPECIALS.values())

    def _parse_pure_text_line(self, line):
        self.html_lines.append(f'<p>{ line }</p>')

    def md_to_html(self):
        return "\n".join(self.html_lines)

    def md_to_html_file(self):
        with open(self.html_file_path, 'wb') as html_file: html_file.write(str(self.html).encode('utf-8'))

if __name__ == "__main__":
    md_text = """# AI Systems Design From Scratch 

> *(Star⭐ our Repo)*

A comprehensive, zero-dependency implementation of artificial intelligence components and enterprise systems design patterns, built completely from first principles.

**Amin Boulouma** — *Software Engineer*

To clone and use the repository, execute:

```git clone https://github.com/aminblm/ai_systems_design_from_scratch.git```

* **PyTorch** (Custom tensor structures and automatic differentiation tracking)
* **Tensorflow** (Alternative computation graph and execution engine)
* **Numpy** (Pure Python multi-dimensional array structures and matrix math routines)
* **Pandas** (DataFrames, Series, and structured data-manipulation mechanics)
* **Ollama** (Local LLM protocol orchestration and serving architecture)
* **Meta’s Llama** (Open-weights inference parser and layer-by-layer execution engine)
* **ChatGPT** (Upstream LLM API integration and chat state wrapper)
"""
    md_to_html = MarkdownToHTML(markdown_text=md_text, html_file_path='src/py_markdown_to_html/md_str_to_html.html')
    print(md_to_html.md_to_html())
    md_to_html.md_to_html_file()

    md_to_html = MarkdownToHTML(markdown_file_path='src/py_markdown_to_html/md_file.md', html_file_path='src/py_markdown_to_html/md_file_to_html.html')
    print(md_to_html.md_to_html())
    md_to_html.md_to_html_file()