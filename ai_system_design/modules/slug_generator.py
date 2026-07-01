# slug_generator.py
import datetime, re, sys, unicodedata

from ai_system_design.kernel.mixins import TestMixin, LoggableMixin


class TestSlugGenerator(TestMixin):
    """Test the slug_generator module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestSlugGenerator initialized.")

    def test(self):
        super().test()
        JekyllFilenameController().start_generator_interface()

class SlugGenerator(LoggableMixin):
    """Handles the transformation of raw text titles into clean, web-safe SEO slugs."""
    
    def __init__(self, allow_unicode: bool = False):
        super().__init__()
        # Allow custom punctuation masks, defaulting to standard string punctuation
        self.allow_unicode = allow_unicode 
        self.logger.info("SlugGenerator initialized.")
        
    def transform_to_slug(self, text: str) -> str:
        """Decomposes, purges, and reformats string text into clean hyphenated tokens."""
        if not text:
            return ""

        # Normalize foreign character accents (e.g., 'Café' becomes 'Cafe' via NFKD decomposition)
        if not self.allow_unicode:
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        else:
            text = unicodedata.normalize('NFKC', text)

        # Force uniform lowercase
        text = text.lower()

        # Purge all remaining invalid non-alphanumeric filesystem symbols using regex patterns
        text = re.sub(r'[^\w\s-]', '', text).strip()

        # Replace clustered spaces or multi-hyphen runs with a single clean hyphen delimiter
        text = re.sub(r'[-\s]+', '-', text)

        return text.strip('-')


class JekyllFilenameController(LoggableMixin):
    """Orchestrates interactive terminal interfaces and handles dynamic filesystem name routing."""

    def __init__(self, generator: SlugGenerator = SlugGenerator(allow_unicode=False)) -> None:
        super().__init__()
        self.generator = generator
        self.logger.info("JekyllFilenameController initialized.")

    @property
    def current_date_string(self) -> str:
        """Dynamically computes the date stamp inline, avoiding stale cached properties over midnights."""
        return datetime.date.today().strftime("%Y-%m-%d")
    
    def print_welcome_banner(self) -> None:
        """Renders structural terminal application interface system frames."""
        print("=========================================================")
        print("     Production Jekyll Post Filename Compiler Engine     ")
        print("         Type 'exit' or use Ctrl+C to terminate.         ")
        print("=========================================================\n")

    def evaluate_line_transaction(self, raw_input: str) -> bool:
        """Validates CLI entries, processes strings, and echoes valid Jekyll paths."""
        cleaned_input = raw_input.strip()

        if cleaned_input.lower() in ('exit', 'quit'):
            print("\nShutting down filename generation engine tools safely.")
            return False

        if not cleaned_input:
            return True

        # Generate slug and prefix path values dynamically
        slug = self.generator.transform_to_slug(cleaned_input)
        
        if not slug:
            print("Error: Input text strings contain no valid alphanumeric naming elements.")
            return True

        # Fetch fresh date data directly from properties loop
        compiled_filename = f"{self.current_date_string}-{slug}.md"

        print("-" * 65)
        print(f"\n[Generated SEO Slug]:\n{slug}")
        print(f"\n[Generated Markdown File name]:\n{compiled_filename}")
        print(f"\n[Jekyll Post Target]:\n_posts/{compiled_filename}")
        print("-" * 65 + "\n")
        return True

    def start_generator_interface(self) -> None:
        """Engages infinite user interface validation entry polling blocks."""
        self.print_welcome_banner()

        while True:
            try:
                print("Enter Article Title -> ", end="", flush=True)
                user_entry = sys.stdin.readline()
                
                # Signal channel dropped via EOF/Null
                if not user_entry:
                    break
                
                should_continue = self.evaluate_line_transaction(user_entry)
                if not should_continue:
                    break

            except (KeyboardInterrupt, SystemExit):
                print("\n\nProcess execution context aborted via hardware signal lines.")
                break