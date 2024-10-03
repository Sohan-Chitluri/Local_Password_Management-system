# Password Managment System
(Under Heavy Development)

## 📖 Overview
This project implements a Password Management System designed to create secure passwords based on user-provided inputs. By employing various transformation algorithms, it ensures that generated passwords contain a mix of uppercase letters and special characters, significantly enhancing their strength.

## 🚀 Features
- User-Centric Design: The system prompts users for their username, website, favorite color, and a unique code word. This information forms the basis of the password generation process.
- Security Through Obscurity: One of the standout features of this system is its ability to protect user passwords even in the event of system compromise. Since passwords are not stored directly and rely on personal questions known only to the user, unauthorized access becomes significantly more challenging for potential hackers.
- Advanced Transformation Algorithms: The project utilizes multiple algorithms to manipulate ASCII values and incorporate character transformations, ensuring that the final passwords are complex and difficult to guess.
- Key File Generation: The code generates a key file that stores important information, such as hashed values and transformation sequences. Without this file, users will not be able to generate their passwords, adding an extra layer of security.
- Storage: Password is never physically stored on Machine!!!

## 📂 Getting Started
### Prerequisites
- Python 3.x
- Required libraries: `json`, `os`, `random`, `hashlib`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sohan-Chitluri/Local_Password_Management-system.git
