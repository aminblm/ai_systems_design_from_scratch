
import re, shutil
from pathlib import Path

        
# --- Configuration & Assets ---
AUTHOR_NAME = "Amin Boulouma"
AUTHOR_LINK = "https://linktr.ee/aminboulouma"
HUB_URL = "https://aminblm.github.io/ai_systems_design_from_scratch/"
BLOG_URL = f"{HUB_URL}blog"
GH_URL = "https://github.com/aminblm/ai_systems_design_from_scratch"

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

PH_BADGE = """
<a href="https://www.producthunt.com/products/ai-systems-design-from-first-principles?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-ai-systems-design-from-first-principles" target="_blank" rel="noopener noreferrer"><img alt="AI Systems Design From First Principles - An implementation of AI Systems Design From First Principles | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1173628&amp;theme=dark&amp;t=1781635927239"></a>
"""

LINKS_DIV = f"""
<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="{HUB_URL}" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">Documentation Hub</a>
  <a href="{BLOG_URL}" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">Engineering Blog</a>
  <a href="{GH_URL}" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">GitHub Repository</a>
</div>
"""

AUTHOR_CARD = f"""
<div class="author-card">
    <p><strong>{AUTHOR_NAME}</strong>, <i>Software Engineer</i></p>
</div>
"""

# --- Transformation Logic ---

def wrap_html_component(content: str) -> str:
    return f"\n\n{content.strip()}\n\n"

def transform_content(content: str) -> str:
    parts = re.split(r'^---', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3: return content
    
    front_matter, body = parts[1], parts[2]
    body = re.sub(r'^\s*---\s*$', '', body, flags=re.MULTILINE)
    
    # 1. Header Assembly
    header = f"{META_TEMPLATE}\n{AUTHOR_LINK_HTML}\n{PH_BADGE}\n{wrap_html_component(LINKS_DIV)}"
    
    # 2. Body Assembly
    # Inject Author Card after first H1
    body = re.sub(r'(# .+\n)', r'\1\n' + wrap_html_component(AUTHOR_CARD) + '\n', body, count=1)
    
    # 3. Footer Assembly
    footer = wrap_html_component(AUTHOR_LINK_HTML)
    
    return f"---\n{front_matter}\n---\n{header}\n{body.strip()}\n\n{footer}"

# --- Execution Engine ---

def run_pipeline(input_dir: Path, output_dir: Path):
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for md_file in input_dir.glob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        transformed = transform_content(content)
        (output_dir / md_file.name).write_text(transformed, encoding='utf-8')
        print(f"Processed: {md_file.name}")
