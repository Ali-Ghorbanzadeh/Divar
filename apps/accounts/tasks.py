from time import sleep
from celery import shared_task
from services.mail import MailProvider


@shared_task
def send_verify_code(email, code):
    print(f"Sending mail to {email}")

    MailProvider(
        "Login/Register CODE",
        email,
        "mail/verify-code.html",
        {"code": code}
    ).send()

    print(f"Email send to {email} !")