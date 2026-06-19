"""
CLI entry point for the Local Password Management System.

This is the interactive front-end.  All core logic lives in
password_manager.py; all character transforms live in transforms.py.
"""

from password_manager import PasswordManager


def get_choice() -> str:
    """Ask whether to retrieve an existing password or create a new one."""
    max_retries = 5
    for attempt in range(max_retries):
        choice = input("Retrieve a password or make a new one? (r/n): ").strip().lower()
        if choice in ("r", "n"):
            return choice
        print(f"Attempt {attempt + 1}/{max_retries}. Please enter 'r' or 'n'.")
    raise SystemExit("Too many invalid attempts. Exiting.")


def get_password_length() -> int:
    """Prompt for desired password length (8–20)."""
    while True:
        try:
            length = int(input("Password length (8–20): "))
            if 8 <= length <= 20:
                return length
            print("Please enter a number between 8 and 20.")
        except ValueError:
            print("Invalid input — enter a number.")


def gather_user_inputs() -> tuple[str, str, str, str]:
    """Prompt the user for credential inputs with a confirmation step."""
    while True:
        username = input("Enter your username: ").strip()
        website = input("Website: ").strip()
        favorite_color = input("Favorite color: ").strip()
        code_word = input("Code word: ").strip()

        confirm = input("Confirm details are correct (y/n): ").strip().lower()
        if confirm == "y":
            return username, website, favorite_color, code_word
        print("Let's try again.\n")


# ── Main ─────────────────────────────────────────────────────────────

def main() -> None:
    manager = PasswordManager("password.json")
    choice = get_choice()

    if choice == "n":
        # ── Create new password ──────────────────────────────────────
        length = get_password_length()
        username, website, favorite_color, code_word = gather_user_inputs()

        password = manager.create_password(
            username, website, favorite_color, code_word, length,
        )
        print(f"\n[OK] Generated password: {password}")

    elif choice == "r":
        # ── Retrieve existing password ───────────────────────────────
        username, website, favorite_color, code_word = gather_user_inputs()

        # Fuzzy website lookup
        matched = manager.find_website(website)
        if not matched:
            print("Cannot retrieve — website not found.")
            return
        website = matched

        password = manager.retrieve_password(
            username, website, favorite_color, code_word,
        )
        if password:
            print(f"\n[KEY] Retrieved password: {password}")
        else:
            print("\n[FAIL] Could not retrieve password. Check your inputs.")


if __name__ == "__main__":
    main()
