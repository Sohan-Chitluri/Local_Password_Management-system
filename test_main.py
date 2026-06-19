"""Tests for the Local Password Management System."""

import json
import os

import pytest

from transforms import (
    ascii_mod_transform,
    ascii_mod_transform_numeric,
    ascii_shift,
    binary_left_shift,
    binary_right_shift,
    binary_xor_fixed,
    binary_inversion,
    rotate_character,
    toggle_even_odd,
    xor_with_value,
    apply_transform,
    TRANSFORMS,
)
from password_manager import PasswordManager


# ═══════════════════════════════════════════════════════════════════════
# Transform Tests
# ═══════════════════════════════════════════════════════════════════════

class TestTransforms:
    """Every transform must accept a char and return a single printable char."""

    SAMPLE_CHARS = list("AZaz09!@# ")

    # ── Individual transforms ────────────────────────────────────────

    def test_ascii_mod_transform(self):
        # 'a' = 97, 97 % 26 = 19, 'A' + 19 = 'T'
        assert ascii_mod_transform('a') == 'T'

    def test_ascii_mod_transform_numeric(self):
        # 'a' = 97, 97 % 10 = 7, '0' + 7 = '7'
        assert ascii_mod_transform_numeric('a') == '7'

    def test_ascii_shift(self):
        result = ascii_shift('A', 7)
        assert result.isprintable()
        assert len(result) == 1

    def test_binary_left_shift_returns_str(self):
        result = binary_left_shift('A')
        assert isinstance(result, str)
        assert len(result) == 1

    def test_binary_right_shift_returns_str(self):
        result = binary_right_shift('A')
        assert isinstance(result, str)
        assert len(result) == 1

    def test_rotate_digit_wraps(self):
        assert rotate_character('9', 3) == '2'

    def test_rotate_lowercase_wraps(self):
        assert rotate_character('z', 3) == 'c'

    def test_rotate_uppercase_wraps(self):
        assert rotate_character('Z', 3) == 'C'

    def test_toggle_even_odd(self):
        # 'B' = 66 (even) → 67 = 'C'
        assert toggle_even_odd('B') == 'C'

    def test_xor_with_value_returns_str(self):
        result = xor_with_value('A')
        assert isinstance(result, str) and len(result) == 1

    def test_binary_inversion_printable(self):
        result = binary_inversion('A')
        assert result.isprintable() and len(result) == 1

    def test_binary_xor_fixed(self):
        result = binary_xor_fixed('A')
        assert isinstance(result, str) and len(result) == 1

    # ── Bulk: every transform on every sample char ───────────────────

    @pytest.mark.parametrize("index", range(len(TRANSFORMS)))
    def test_all_transforms_produce_single_printable(self, index):
        for ch in self.SAMPLE_CHARS:
            result = apply_transform(ch, index)
            assert isinstance(result, str), f"Transform {index} on '{ch}' returned non-str"
            assert len(result) == 1, f"Transform {index} on '{ch}' returned len != 1"
            assert result.isprintable(), f"Transform {index} on '{ch}' not printable"

    def test_apply_transform_wraps_index(self):
        """Index > 9 wraps via modulo."""
        assert apply_transform('A', 10) == apply_transform('A', 0)


# ═══════════════════════════════════════════════════════════════════════
# PasswordManager Tests
# ═══════════════════════════════════════════════════════════════════════

class TestPasswordManager:
    """Core password generation and retrieval logic."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Fresh PasswordManager with a temp key file."""
        return PasswordManager(str(tmp_path / "test_keys.json"))

    # ── Key file ─────────────────────────────────────────────────────

    def test_keyfile_created_on_init(self, manager):
        assert os.path.exists(manager.filename)

    def test_keyfile_has_25_sequences(self, manager):
        assert len(manager.data["sequences"]) == 25

    def test_sequences_are_21_digits(self, manager):
        for seq in manager.data["sequences"]:
            assert 10**20 <= seq < 10**21

    # ── Creating passwords ───────────────────────────────────────────

    def test_create_returns_correct_length(self, manager):
        pw = manager.create_password("user", "site.com", "blue", "word", 12)
        assert len(pw) == 12

    def test_create_stores_entry(self, manager):
        manager.create_password("alice", "github.com", "red", "code", 10)
        assert "github.com" in manager.data["website"]
        assert "alice" in manager.data["username"]

    def test_salt_stored_per_entry(self, manager):
        manager.create_password("u1", "s1.com", "c1", "w1", 8)
        manager.create_password("u2", "s2.com", "c2", "w2", 8)
        assert len(manager.data["salt"]) == 2
        assert manager.data["salt"][0] != manager.data["salt"][1]

    # ── Retrieving passwords ─────────────────────────────────────────

    def test_retrieve_matches_create(self, manager):
        """Same inputs + same key file → identical password."""
        pw1 = manager.create_password("alice", "github.com", "red", "code", 16)
        pw2 = manager.retrieve_password("alice", "github.com", "red", "code")
        assert pw1 == pw2

    def test_retrieve_nonexistent_returns_none(self, manager):
        assert manager.retrieve_password("x", "nope.com", "z", "q") is None

    def test_wrong_inputs_return_none(self, manager):
        manager.create_password("alice", "github.com", "red", "code", 10)
        # Wrong color → hash won't match any answer
        result = manager.retrieve_password("alice", "github.com", "WRONG", "code")
        assert result is None

    # ── Different sites → different passwords ────────────────────────

    def test_different_sites_different_passwords(self, manager):
        pw1 = manager.create_password("bob", "site1.com", "green", "w", 10)
        pw2 = manager.create_password("bob", "site2.com", "green", "w", 10)
        assert pw1 != pw2

    # ── Persistence ──────────────────────────────────────────────────

    def test_keyfile_persists_across_loads(self, manager):
        manager.create_password("user", "x.com", "c", "w", 8)
        # Reload from the same file
        manager2 = PasswordManager(manager.filename)
        pw = manager2.retrieve_password("user", "x.com", "c", "w")
        assert pw is not None

    # ── Website lookup ───────────────────────────────────────────────

    def test_find_website_exact(self, manager):
        manager.create_password("u", "github.com", "c", "w", 8)
        assert manager.find_website("github.com") == "github.com"

    def test_find_website_not_found(self, manager):
        assert manager.find_website("nonexistent.com") is None
