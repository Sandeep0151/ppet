import secrets
from django.core.mail import send_mail
from .models import Profile


def generate_unique_token():
    return secrets.token_hex(20)


def send_reset_password_email(user):
    token = generate_unique_token()
    profile, created = Profile.objects.get_or_create(user=user)
    profile.forgot_password_token = token
    profile.save()

    reset_link = f"http://192.168.0.247:8000/reset-password/{token}/"
    subject = "Reset Your Password"
    message = f"Click on the following link to reset your password: {reset_link}"
    recipient_list = [user.email]

    send_mail(subject, message, from_email=None, recipient_list=recipient_list)
