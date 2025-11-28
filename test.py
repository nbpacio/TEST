"""
This script prompts the user for their first and last name,
and then prints a greeting.
"""

def main() -> None:
    """Gets the user's name and prints a greeting."""
    first_name: str = input("What is your first name: ")
    last_name: str = input("What is your last name: ")
    full_name = f"{first_name} {last_name}"
    print(f"Hello, {full_name}!")

if __name__ == "__main__":
    main()