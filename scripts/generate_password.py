"""Generate a password hash for a user.

Steps:
1. Run the script: `python scripts/generate_password.py`.
2. Take the output and put it in the database.
3. Communicate the password to the user over a secure channel.
"""

import bcrypt

password = input("Please enter your password: ")
password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
    "utf-8",
)
print(f"Password hash: {password_hash}")  # noqa: T201 - Print.
