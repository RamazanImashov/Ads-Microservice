from django.utils import timezone
from datetime import timedelta
from config.setting.hepler.celery import app
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail

from .SendSms import send_sms

User = get_user_model()


def send_activation_code(username, email, activation_code):
    context = {
        "text_detail": "Thank you for registration",
        "username": username,
        "email": email,
        "domain": "http://127.0.0.1:8003/",
        "activation_code": activation_code,
    }
    message_html = render_to_string("email_url.html", context)
    message = strip_tags(message_html)
    send_mail(
        "Activation accounts",
        message,
        "admin@gmail.com",
        [email],
        html_message=message_html,
        fail_silently=False,
    )

@app.task
def send_activation_code_celery(username, email, activation_code):
    send_activation_code(username, email, activation_code)

def send_password(username, email, activation_code):
    context = {
        "text_detail": "Password recovery",
        "username": username,
        "email": email,
        "forgot_password_code": activation_code,
    }
    message_html = render_to_string("lose_password.html", context)
    message = strip_tags(message_html)
    send_mail(
        "Password recovery",
        message,
        "admin@gmail.com",
        [email],
        html_message=message_html,
        fail_silently=False,
    )


@app.task
def send_password_celery(username, email, activation_code):
    send_password(username, email, activation_code)


@shared_task
def delete_unconfirmed_users():
    expiration_time = timezone.now() - timedelta(minutes=1)
    User.objects.filter(is_active=False, date_joined__lt=expiration_time).delete()


@app.task
def send_sms_task(username, phone, verify_code):
    send_sms(username, phone, verify_code)
