import secrets
import string


def create_token() -> str:
    number = string.digits
    token = ''.join(secrets.choice(number) for i in range(6))
    return token