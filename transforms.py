"""
Character transformation functions for password generation.

Each function takes a single printable ASCII character and returns
a single printable ASCII character.  All outputs are guaranteed to
be in the printable range (32–126).
"""


def ascii_mod_transform(char: str, base: str = 'A') -> str:
    """Map character to a letter by taking ASCII value mod 26."""
    return chr(ord(base) + ord(char) % 26)


def ascii_mod_transform_numeric(char: str) -> str:
    """Map character to a digit by taking ASCII value mod 10."""
    return chr(ord('0') + ord(char) % 10)


def ascii_shift(char: str, shift_value: int = 7) -> str:
    """Shift ASCII value by a fixed amount, wrapping within printable range."""
    return chr((ord(char) - 32 + shift_value) % 95 + 32)


def binary_left_shift(char: str) -> str:
    """Perform a binary left shift on the character's ASCII value."""
    shifted = (ord(char) << 1) % 128
    if 32 <= shifted <= 126:
        return chr(shifted)
    return chr(shifted % 95 + 32)


def binary_right_shift(char: str) -> str:
    """Perform a binary right shift on the character's ASCII value."""
    shifted = ord(char) >> 1
    if 32 <= shifted <= 126:
        return chr(shifted)
    return chr(shifted % 95 + 32)


def rotate_character(char: str, value: int = 3) -> str:
    """Rotate digits within 0-9, lowercase within a-z, uppercase within A-Z."""
    if char.isdigit():
        return chr((ord(char) - 48 + value) % 10 + 48)
    if char.islower():
        return chr((ord(char) - 97 + value) % 26 + 97)
    if char.isupper():
        return chr((ord(char) - 65 + value) % 26 + 65)
    return char


def toggle_even_odd(char: str) -> str:
    """Toggle between even and odd ASCII values (+1 if even, -1 if odd)."""
    val = ord(char)
    toggled = val + 1 if val % 2 == 0 else val - 1
    if 32 <= toggled <= 126:
        return chr(toggled)
    return char  # edge case: stay put if toggle leaves printable range


def xor_with_value(char: str, xor_value: int = 5) -> str:
    """XOR the character's ASCII value with a fixed value."""
    if char.isdigit():
        result = (ord(char) - 48) ^ xor_value
        return chr((result % 10) + 48)
    result = ord(char) ^ xor_value
    if 32 <= result <= 126:
        return chr(result)
    return chr(result % 95 + 32)


def binary_inversion(char: str) -> str:
    """Invert bits of the character's ASCII value (7-bit)."""
    inverted = ~ord(char) & 0x7F
    if 32 <= inverted <= 126:
        return chr(inverted)
    return chr(inverted % 95 + 32)


def binary_xor_fixed(char: str, xor_value: int = 2) -> str:
    """XOR with a small fixed value."""
    result = ord(char) ^ xor_value
    if 32 <= result <= 126:
        return chr(result)
    return chr(result % 95 + 32)


# ── Transform Registry ──────────────────────────────────────────────

TRANSFORMS = [
    ascii_mod_transform,           # 0
    ascii_mod_transform_numeric,   # 1
    ascii_shift,                   # 2
    binary_left_shift,             # 3
    binary_right_shift,            # 4
    rotate_character,              # 5
    toggle_even_odd,               # 6
    xor_with_value,                # 7
    binary_inversion,              # 8
    binary_xor_fixed,              # 9
]


def apply_transform(char: str, transform_index: int) -> str:
    """Apply a character transformation selected by index (wraps mod 10)."""
    return TRANSFORMS[transform_index % len(TRANSFORMS)](char)
