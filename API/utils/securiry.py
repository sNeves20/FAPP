import bcrypt
from getpass import getpass

SECRET_KEY = bcrypt.gensalt(rounds=16)

def hash_password(password: str):
    hashed_password = bcrypt.hashpw(password.encode(), SECRET_KEY)

    return hashed_password

def check_hash(password: str, hashed_password: str) -> bool:

    valid = bcrypt.checkpw(password.encode(), hashed_password.encode())

    return valid 