from django.core.mail import send_mail
from django.conf import settings

import string
import secrets


def generate_otp_code():
    return str("".join(secrets.choice(string.digits) for _ in range(6)))


def send_email_user_otp(user_otp_code, user_email):
    send_mail(
        "Verification OTP",
        f"Your OTP for account verification is {user_otp_code}",
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )