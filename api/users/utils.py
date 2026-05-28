import string
import secrets


def generate_otp_code():
    return int("".join(secrets.choice(string.digits) for _ in range(6)))
