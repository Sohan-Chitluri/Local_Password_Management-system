# Password Management System

## 📖 Overview
A local password management system that **generates** passwords deterministically from user-provided inputs — without ever storing the passwords themselves. If you supply the same inputs with the same key file, you get the same password back.

## 🚀 Features
- **Zero password storage** — passwords are re-derived on the fly, never saved to disk.
- **Cryptographically secure randomness** — uses Python's `secrets` module (CSPRNG) instead of `random`.
- **Salted, key-stretched hashes** — PBKDF2-HMAC-SHA256 with 100 000 iterations and per-entry salts.
- **Rich password output** — BLAKE2s binary digest mapped to 90+ characters (upper, lower, digits, symbols) with per-character transforms.
- **Fuzzy website matching** — catches typos when retrieving passwords.
- **Key file** (`password.json`) — stores hashed metadata required for password re-derivation. Losing this file means losing access to all generated passwords.

## 📂 Project Structure
```
├── main.py              # CLI entry point
├── password_manager.py  # Core logic (PasswordManager class)
├── transforms.py        # 10 character transformation functions
├── test_main.py         # Pytest test suite
├── Readme.md
└── License
```

## ⚡ Getting Started

### Prerequisites
- Python 3.10+
- `pytest` (for running tests)

### Installation
```bash
git clone https://github.com/Sohan-Chitluri/Local_Password_Management-system.git
cd Local_Password_Management-system
```

### Usage
```bash
python main.py
```
You'll be prompted to **create** (`n`) or **retrieve** (`r`) a password.

### Running Tests
```bash
python -m pytest test_main.py -v
```

## 🔐 Security Model
| Layer | Mechanism |
|-------|-----------|
| Randomness | `secrets` module (CSPRNG) |
| Input hashing | PBKDF2-HMAC-SHA256, 100k iterations, per-entry salt |
| Sequence selection | 25 cryptographically random 21-digit numbers |
| Password derivation | BLAKE2s digest → per-character transform chain |
| File permissions | Owner-only (`0o600`) on key file creation |

> ⚠️ **Important:** The key file (`password.json`) is essential. Back it up securely — without it, passwords cannot be re-derived. Future versions will add at-rest encryption with a master passphrase.

## 📜 License
MIT — see [License](License) for details.
