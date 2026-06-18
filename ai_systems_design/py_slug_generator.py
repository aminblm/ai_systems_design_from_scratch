import datetime
import string

class SlugGenerator:
    """Handles the transformation of raw text titles into clean, web-safe SEO slugs."""
    
    def __init__(self, punctuation_mask=None):
        # Allow custom punctuation masks, defaulting to standard string punctuation
        self.punctuation_mask = punctuation_mask if punctuation_mask is not None else string.punctuation

    def clean_title(self, title: str) -> str:
        """Forces lowercase normalization and purges masked punctuation characters."""
        if not title: return ""
        lowercase_title = title.lower()
        return "".join(char for char in lowercase_title if char not in self.punctuation_mask)

    def build_slug(self, title: str) -> str:
        """Transforms a raw title into a standard hyphenated url token block."""
        cleaned = self.clean_title(title)
        tokens = cleaned.split()
        return "-".join(tokens)


class TerminalInterface:
    """Manages the terminal input/output state machine and interactive loop logic."""
    
    def __init__(self, generator: SlugGenerator):
        self.generator = generator
        # Cache today's prefix date string inside instance memory state
        self.date_prefix = datetime.date.today().strftime("%Y-%m-%d")

    def display_header(self):
        """Renders the standard UI layout system boundaries."""
        print("=========================================================")
        print("    OOP Jekyll Blog Post Filename Generator Engine       ")
        print("        Type 'exit' or 'quit' to terminate.              ")
        print("=========================================================\n")

    def process_input(self, user_input: str) -> bool:
        """
        Evaluates input tokens. Returns False if a shutdown token is 
        received, otherwise processes text parameters and returns True.
        """
        cleaned_input = user_input.strip()
        
        if cleaned_input.lower() in ['exit', 'quit']:
            print("\nShutdown sequence initiated. Goodbye.")
            return False
            
        if not cleaned_input:
            return True
            
        # Invoke the aggregated generator service dependency
        slug = self.generator.build_slug(cleaned_input)
        filename = f"{self.date_prefix}-{slug}.md"
        
        print("-" * 60)
        print(f"Target Slug    : {slug}")
        print(f"Jekyll File    : _posts/{filename}")
        print("-" * 60 + "\n")
        return True

    def run(self):
        """Ignites the infinite polling loop execution layer."""
        self.display_header()
        
        while True:
            try:
                raw_input = input("Enter Blog Title -> ")
                should_continue = self.process_input(raw_input)
                if not should_continue: break
            except (KeyboardInterrupt, EOFError):
                print("\n\nProcess interrupted via runtime signal. Exiting safely.")
                break


if __name__ == "__main__":
    # 1. Instantiate the atomic logic engine worker
    slug_engine = SlugGenerator()
    
    # 2. Inject the worker instance dependency straight into the Interface Controller
    interface = TerminalInterface(generator=slug_engine)
    
    # 3. Trigger the runtime framework loop
    interface.run()