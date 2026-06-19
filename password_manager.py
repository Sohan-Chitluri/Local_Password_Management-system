"""
Core password management logic.

Security improvements over the original:
- Uses `secrets` module instead of `random` (CSPRNG vs Mersenne Twister).
- Salts every stored hash with a per-entry random salt.
- Uses PBKDF2-HMAC-SHA256 (100 000 iterations) instead of plain SHA-256.
- Applies per-character transforms using sequence digits, not a single value.
- Maps BLAKE2s binary digest to a rich 90+ character output set.
- Restricts key-file permissions to owner-only on creation.
"""

import hashlib
import json
import os
import secrets
import stat
from typing import Optional

from transforms import apply_transform


# Rich character set for password output mapping
PASSWORD_CHARSET = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "!@#$%^&*()-_=+[]{}|;:,.<>?"
)


class PasswordManager:
    """Manages password generation and retrieval using a local key file."""

    def __init__(self, filename: str = "password.json"):
        self.filename = filename
        self.data = self._load_or_create_keyfile()

    # ── Key-File Operations ──────────────────────────────────────────

    def _load_or_create_keyfile(self) -> dict:
        """Load existing key file or create a new one."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
            print(f"Loaded key file: {self.filename}")
            return data

        data = {
            "sequences": [],
            "website": [],
            "username": [],
            "base_hash": [],
            "sequence_hash": [],
            "salt": [],
            "length_of_password": [],
            "version": [],
            "created_at": [],
        }
        self._generate_sequences(data)
        self._save(data)

        # Restrict file permissions to owner-only
        try:
            os.chmod(self.filename, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass  # Windows may not fully support Unix permissions

        print(f"Created new key file: {self.filename}")
        return data

    @staticmethod
    def _generate_sequences(data: dict, count: int = 25) -> None:
        """Generate cryptographically secure random 21-digit sequences."""
        lower = 10**20
        upper = 10**21 - 1
        for _ in range(count):
            data["sequences"].append(secrets.randbelow(upper - lower) + lower)

    def _save(self, data: Optional[dict] = None) -> None:
        """Persist data to the key file."""
        if data is None:
            data = self.data
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    # ── Website Lookup ───────────────────────────────────────────────

    def find_website(self, website: str) -> Optional[str]:
        """Look up a website with fuzzy matching for typos.

        Returns the matched website name, or None.
        """
        existing = self.data["website"]

        # Exact match
        if website in existing:
            print(f"Found account for: {website}")
            return website

        # Fuzzy match (> 70 % character overlap)
        threshold = 0.70
        candidates = []
        for stored in existing:
            matches = sum(1 for a, b in zip(website, stored) if a == b)
            similarity = matches / max(len(website), 1)
            if similarity > threshold:
                candidates.append(stored)

        if not candidates:
            print("No matching website found.")
            return None

        if len(candidates) == 1:
            print(f"Did you mean: {candidates[0]}?")
            return candidates[0]

        # Multiple candidates — let the user pick
        print("Did you mean one of these?")
        for i, name in enumerate(candidates):
            print(f"  {i}) {name}")

        while True:
            try:
                choice = int(input("Enter the number: "))
                if 0 <= choice < len(candidates):
                    return candidates[choice]
                print(f"Please enter 0–{len(candidates) - 1}.")
            except ValueError:
                print("Please enter a valid number.")

    # ── Answer Generation ────────────────────────────────────────────

    @staticmethod
    def _generate_answers(
        username: str, website: str,
        favorite_color: str, code_word: str,
    ) -> list[str]:
        """Build deterministic answer combinations from user inputs."""
        return [
            username + website + favorite_color,
            website[2:3] + favorite_color[4:5] + code_word,
            f"{username}_{website}",
            f"{favorite_color}_{website}",
            f"{username[:3]}{favorite_color}{website[-3:]}",
        ]

    # ── Hash Helpers ─────────────────────────────────────────────────

    @staticmethod
    def _hash_with_salt(value: str, salt: str) -> str:
        """PBKDF2-HMAC-SHA256 hash with 100 000 iterations."""
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            value.encode(),
            salt.encode(),
            iterations=100_000,
        )
        return dk.hex()

    # ── Create Password ──────────────────────────────────────────────

    def create_password(
        self,
        username: str, website: str,
        favorite_color: str, code_word: str,
        length: int,
        version: int = 1,
    ) -> str:
        """Create and store a new password entry; returns the password."""
        answers = self._generate_answers(
            username, website, favorite_color, code_word,
        )

        # Select a random answer and sequence (cryptographically secure)
        answer_index = secrets.randbelow(len(answers))
        selected_answer = answers[answer_index]
        selected_sequence = secrets.choice(self.data["sequences"])

        # Per-entry random salt
        salt = secrets.token_hex(16)

        # Store hashed values — never the raw answer
        answer_hash = self._hash_with_salt(selected_answer, salt)
        sequence_hash = hashlib.sha256(
            str(selected_sequence).encode(),
        ).hexdigest()

        self.data["username"].append(username)
        self.data["website"].append(website)
        self.data["base_hash"].append(answer_hash)
        self.data["sequence_hash"].append(sequence_hash)
        self.data["salt"].append(salt)
        self.data["length_of_password"].append(length)
        self.data["version"].append(1)  # initial version
        self._save()

        # Use each digit of the sequence for per-character transforms
        sequence_digits = [int(d) for d in str(selected_sequence)]

        return self._generate_password(
            answer_index, sequence_digits, answers, length,
        )

    # ── Retrieve Password ────────────────────────────────────────────

    def retrieve_password(
        self,
        username: str, website: str,
        favorite_color: str, code_word: str,
    ) -> Optional[str]:
        """Re-derive a previously generated password from the same inputs."""
        answers = self._generate_answers(
            username, website, favorite_color, code_word,
        )

        # Locate the website entry
        website_index = None
        for i, w in enumerate(self.data["website"]):
            if w == website:
                website_index = i
                break

        if website_index is None:
            print("Website entry not found in key file.")
            return None

        # Identify which answer combination was used
        stored_hash = self.data["base_hash"][website_index]
        salt = self.data["salt"][website_index]

        answer_index = None
        for i, ans in enumerate(answers):
            if self._hash_with_salt(ans, salt) == stored_hash:
                answer_index = i
                break

        if answer_index is None:
            print("Could not match inputs — did you enter the same details?")
            return None

        # Recover the sequence by matching its hash
        stored_seq_hash = self.data["sequence_hash"][website_index]
        selected_sequence = None
        for seq in self.data["sequences"]:
            if hashlib.sha256(str(seq).encode()).hexdigest() == stored_seq_hash:
                selected_sequence = seq
                break

        if selected_sequence is None:
            print("Sequence not found — key file may be corrupted.")
            return None

        sequence_digits = [int(d) for d in str(selected_sequence)]
        length = self.data["length_of_password"][website_index]

        return self._generate_password(
            answer_index, sequence_digits, answers, length,
        )

    # ── Password Generation Engine ───────────────────────────────────

    @staticmethod
    def _generate_password(
        answer_index: int,
        sequence_digits: list[int],
        answers: list[str],
        length: int,
    ) -> str:
        """Generate a password by transforming a BLAKE2s digest.

        Uses the full binary digest (256 possible byte values per position)
        mapped to a rich 90+ character set, with a different transform
        applied per character based on the sequence digits.
        """
        digest = hashlib.blake2s(
            answers[answer_index].encode("utf-8"),
        ).digest()  # 32 bytes (values 0–255)

        password_chars: list[str] = []
        for i in range(length):
            # Select transform from the corresponding sequence digit
            transform_idx = sequence_digits[i % len(sequence_digits)]

            # Map digest byte → rich character set
            byte_val = digest[i % len(digest)]
            base_char = PASSWORD_CHARSET[byte_val % len(PASSWORD_CHARSET)]

            # Apply per-character transform
            password_chars.append(apply_transform(base_char, transform_idx))

        return "".join(password_chars)
