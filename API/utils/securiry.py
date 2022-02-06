""" Module in charge of security handeling """

import bcrypt

SECRET_KEY = bcrypt.gensalt(rounds=16)


def hash_password(password: str) -> bytes:
    """Will hash the given password and return the hash result"""

    hashed_password = bcrypt.hashpw(password.encode(), SECRET_KEY)

    return hashed_password


def check_hash(password: str, hashed_password: str) -> bool:
    """Will check if the given password matches the given hash"""

    valid = bcrypt.checkpw(password.encode(), hashed_password.encode())

    return valid
