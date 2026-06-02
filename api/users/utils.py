from django.core.mail import send_mail
import string
import secrets


def generate_otp_code():
    return int("".join(secrets.choice(string.digits) for _ in range(6)))


def send_email_user_otp(user_otp_code, user_email):
    send_mail(
        "Verification OTP",
        f"Your OTP for account verification is {user_otp_code}",
        "admin@example.com",
        [user_email],
        fail_silently=False,
    )