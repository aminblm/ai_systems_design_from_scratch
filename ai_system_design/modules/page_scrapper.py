import urllib.request
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = "No title found"
        self.links = []
        self.current_link = None

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "a":
            # Extract the href attribute from the list of attributes
            for attr, value in attrs:
                if attr == "href":
                    self.current_link = value
                    break

    def handle_data(self, data):
        if self.in_title:
            self.title = data
        elif self.current_link is not None:
            # Store link and the associated text
            self.links.append((self.current_link, data.strip()))
            self.current_link = None

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

def scrape_webpage(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')

        parser = MyHTMLParser()
        parser.feed(html_content)

        print(f"Page Title: {parser.title}")
        print("-" * 30)
        print("Links found:")
        for href, text in parser.links:
            if text: # Only print if there is visible link text
                if href.strip().startswith("/ai"):
                    href = "https://aminblm.github.io" + href.strip()
                    print(f"[{text}]({href})")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_webpage("https://aminblm.github.io/ai_systems_design_from_scratch/blog/")