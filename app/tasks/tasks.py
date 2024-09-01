from pydantic import EmailStr
import smtplib

from app.config import settings
from app.tasks.celery_app import celery
from app.tasks.email_templates import create_reminder

@celery.task
def send_reminder(
    note: dict,
    email_to: EmailStr
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_reminder(note, email_to_mock)
    
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)