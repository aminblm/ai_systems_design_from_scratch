import os
import re
import argparse

# Configuration
AUTHOR_NAME = "Amin Boulouma"
AUTHOR_LINK = "https://linktr.ee/aminboulouma"
HUB_URL = "https://aminblm.github.io/ai_systems_design_from_scratch/"
BLOG_URL = f"{HUB_URL}blog"
GH_URL = "https://github.com/aminblm/ai_systems_design_from_scratch"

# Templates
META_TEMPLATE = """
<head>
  <meta charset="utf-8">
  <title>{{ page.title }} | {{ site.title }}</title>
  <meta name="description" content="{{ page.description | default: site.description }}">
  <link rel="canonical" href="{{ site.url }}{{ site.baseurl }}{{ page.url }}">
  
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{ page.title }}">
  <meta property="og:description" content="{{ page.description | default: site.description }}">
  <meta property="og:url" content="{{ site.url }}{{ site.baseurl }}{{ page.url }}">
  <meta property="og:site_name" content="{{ site.title }}">
  
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{{ page.title }}">
  <meta name="twitter:description" content="{{ page.description | default: site.description }}">
</head>
"""

AUTHOR_LINK_HTML = f"""
<a href="{AUTHOR_LINK}" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with {AUTHOR_NAME} Official
</a>
"""

LINKS_DIV = f"""
<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="{HUB_URL}" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="{BLOG_URL}" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="{GH_URL}" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>
"""

AUTHOR_CARD = """
<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>
"""

def wrap_raw(content):
    """Wraps the content in Jekyll raw tags."""
    return f"{{% raw %}}\n{content}\n{{% endraw %}}\n"

def process_posts(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            parts = re.split(r'^---', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3: continue
            
            front_matter, body = parts[1], parts[2]
            
            # Clean body of redundant horizontal rules
            body = re.sub(r'^\s*---\s*$', '', body, flags=re.MULTILINE)
            
            # Reconstruct with Metas and wrapped HTML elements
            new_content = f"---\n{front_matter}\n---\n{META_TEMPLATE}\n{wrap_raw(AUTHOR_LINK_HTML + '\n' + LINKS_DIV)}\n{body}"
            
            # Insert Author Card after the first H1
            new_content = re.sub(r'(# .+\n)', r'\1\n' + wrap_raw(AUTHOR_CARD) + '\n', new_content, count=1)
            
            # Append Footer
            new_content = new_content.rstrip() + "\n\n" + wrap_raw("\n" + AUTHOR_LINK_HTML) + "\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Processed: {filename} -> {output_dir}")

def clean_posts(input_dir, output_dir):
    """
    Standardizes Markdown files by stripping non-breaking spaces 
    and redundant separators to ensure Jekyll renders HTML correctly.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Remove non-breaking spaces (Unicode U+00A0)
            content = content.replace('\u00a0', ' ')
            
            # 2. Clean up redundant horizontal rules (---) inside body
            # Split only on the first YAML boundary
            parts = re.split(r'^---', content, maxsplit=2, flags=re.MULTILINE)
            if len(parts) < 3: continue
            
            front_matter, body = parts[1], parts[2]
            
            # Remove isolated --- lines
            body = re.sub(r'^\s*---\s*$', '', body, flags=re.MULTILINE)
            
            # 3. Ensure double newline between HTML and Markdown
            # This is critical for Jekyll HTML rendering
            body = re.sub(r'(</div>|</a>)\s*\n(?=#)', r'\1\n\n\n', body)
            
            # Write cleaned file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"---\n{front_matter}\n---\n{body}")
            
            print(f"Cleaned: {filename}")    

def clean_author(input_dir, output_dir):
    """
    Sanitizes markdown files, injects components, and standardizes Jekyll rendering.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Regex to capture the {% raw %} wrapped author card block
    raw_author_pattern = re.compile(
        r'\{%\s*raw\s*%\}\s*<div class="author-card">\s*<p><strong>\{\{\s*site\.author\.name\s*\}\}</strong>\s*—\s*<i>\{\{\s*site\.author\.bio\s*\}\}</i></p>\s*</div>\s*\{%\s*endraw\s*%\}',
        re.MULTILINE
    )

    clean_author_html = """<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>"""

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. PURGE INVISIBLE CHARACTERS
            # Remove non-breaking spaces (U+00A0) and other hidden control chars
            content = content.replace('\u00a0', ' ')
            
            # 2. REPLACE WRAPPED AUTHOR CARD
            content = raw_author_pattern.sub(clean_author_html, content)
            
            # 3. ENSURE RENDERING SPACING
            # Force empty lines around div/a blocks if they precede headers
            content = re.sub(r'(</div>|</a>)\s*\n(?=#)', r'\1\n\n\n', content)
            
            # Remove isolated horizontal rules
            content = re.sub(r'^\s*---\s*$', '', content, flags=re.MULTILINE)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Sanitized and Updated: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Markdown files.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    process_posts(args.input, args.output)