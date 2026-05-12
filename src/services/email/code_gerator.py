import secrets
import string

#simple function for create token, choice a number(0 at 9) in range 6 spaces
def create_token():
    number = string.digits
    token = ''.join(secrets.choice(number) for i in range(6))
    return token