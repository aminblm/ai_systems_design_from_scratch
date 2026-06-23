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

def process_posts(input_dir, output_dir):
    """
    Parses MD files from input_dir, injects elements, 
    and saves to output_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            parts = re.split(r'^---', content, flags=re.MULTILINE)
            if len(parts) < 3: continue
            
            front_matter, body = parts[1], parts[2]
            
            # Reconstruction Logic
            new_content = f"---\n{front_matter}\n---\n{META_TEMPLATE}\n{AUTHOR_LINK_HTML}\n{LINKS_DIV}\n{body}"
            new_content = re.sub(r'(# .+\n)', r'\1\n' + AUTHOR_CARD + '\n', new_content, count=1)
            new_content = new_content.rstrip() + "\n\n---\n" + AUTHOR_LINK_HTML + "\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Processed: {filename} -> {output_dir}")
