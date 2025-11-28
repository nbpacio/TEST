"""
Advanced user interaction script with multiple operation modes.

This script provides a flexible command-line interface for user interaction,
supporting interactive mode, direct command-line arguments, and file-based input.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional


class UserGreeter:
    """Handles user greeting operations with various input methods."""

    def __init__(self, log_level: str = "INFO") -> None:
        """
        Initialize the UserGreeter with logging configuration.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)

    def setup_logging(self, log_level: str) -> None:
        """
        Configure logging with the specified level.

        Args:
            log_level: Logging level as string
        """
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            numeric_level = logging.INFO

        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def validate_name(self, name: str, field_name: str = "Name") -> bool:
        """
        Validate that a name is not empty and contains valid characters.

        Args:
            name: The name to validate
            field_name: The field name for error messages

        Returns:
            True if valid, False otherwise
        """
        if not name or not name.strip():
            self.logger.error(f"{field_name} cannot be empty")
            return False

        if not all(c.isalpha() or c.isspace() or c in "'-" for c in name):
            self.logger.error(f"{field_name} contains invalid characters")
            return False

        return True

    def greet_user(self, first_name: str, last_name: str, title: Optional[str] = None) -> str:
        """
        Generate a greeting message for the user.

        Args:
            first_name: User's first name
            last_name: User's last name
            title: Optional title (Mr., Ms., Dr., etc.)

        Returns:
            The formatted greeting string
        """
        self.logger.debug(f"Generating greeting for {first_name} {last_name}")

        if title:
            full_name = f"{title} {first_name} {last_name}"
        else:
            full_name = f"{first_name} {last_name}"

        greeting = f"Hello, {full_name}!"
        self.logger.info(f"Generated greeting: {greeting}")
        return greeting

    def interactive_mode(self) -> None:
        """Run in interactive mode, prompting user for input."""
        self.logger.info("Starting interactive mode")
        print("=== Interactive Greeting Mode ===")

        while True:
            try:
                first_name = input("What is your first name (or 'quit' to exit): ").strip()

                if first_name.lower() == "quit":
                    print("Goodbye!")
                    break

                if not self.validate_name(first_name, "First name"):
                    continue

                last_name = input("What is your last name: ").strip()
                if not self.validate_name(last_name, "Last name"):
                    continue

                title = input("Title (optional, press Enter to skip): ").strip()
                if title and not self.validate_name(title, "Title"):
                    continue

                greeting = self.greet_user(first_name, last_name, title if title else None)
                print(greeting)
                print()

            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Goodbye!")
                break
            except EOFError:
                print("\nEnd of input. Goodbye!")
                break

    def process_from_file(self, file_path: Path) -> None:
        """
        Process names from a file and generate greetings.

        File format: Each line should contain "FirstName LastName [Title]"

        Args:
            file_path: Path to the input file
        """
        self.logger.info(f"Processing file: {file_path}")

        try:
            if not file_path.exists():
                self.logger.error(f"File not found: {file_path}")
                print(f"Error: File '{file_path}' not found")
                return

            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()
                    if len(parts) < 2:
                        self.logger.warning(f"Line {line_num}: Invalid format - {line}")
                        continue

                    first_name = parts[0]
                    last_name = parts[1]
                    title = parts[2] if len(parts) > 2 else None

                    if self.validate_name(first_name, "First name") and \
                       self.validate_name(last_name, "Last name"):
                        greeting = self.greet_user(first_name, last_name, title)
                        print(greeting)

        except Exception as e:
            self.logger.error(f"Error processing file: {e}")
            print(f"Error processing file: {e}")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Advanced user greeting script with multiple operation modes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python test.py

  # Direct greeting
  python test.py --first-name John --last-name Doe

  # With title
  python test.py --first-name Jane --last-name Smith --title Dr.

  # From file
  python test.py --file names.txt

  # With debug logging
  python test.py --log-level DEBUG
        """,
    )

    parser.add_argument(
        "--first-name",
        "-f",
        type=str,
        help="First name for direct greeting mode",
    )

    parser.add_argument(
        "--last-name",
        "-l",
        type=str,
        help="Last name for direct greeting mode",
    )

    parser.add_argument(
        "--title",
        "-t",
        type=str,
        help="Optional title (Mr., Ms., Dr., etc.)",
    )

    parser.add_argument(
        "--file",
        type=Path,
        help="Process names from a file (one per line: 'FirstName LastName [Title]')",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for the script."""
    args = parse_arguments()

    greeter = UserGreeter(log_level=args.log_level)

    # File mode
    if args.file:
        greeter.process_from_file(args.file)
        return

    # Direct mode
    if args.first_name and args.last_name:
        if greeter.validate_name(args.first_name, "First name") and \
           greeter.validate_name(args.last_name, "Last name"):
            greeting = greeter.greet_user(args.first_name, args.last_name, args.title)
            print(greeting)
        else:
            sys.exit(1)
        return

    # Interactive mode (default)
    if args.first_name or args.last_name:
        print("Error: Both --first-name and --last-name are required for direct mode")
        sys.exit(1)

    greeter.interactive_mode()


if __name__ == "__main__":
    main()
