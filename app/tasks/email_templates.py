from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings

def create_reminder(
    note: dict,
    email_to: EmailStr
):
    email = EmailMessage()
    
    email["Subject"] = "Напоминание о запланированных задачах"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    # if len(notes) > 0:
    #     message = sum([f"{el['note']}\n" for el in notes])  
    # else:
    #     message = "Сегодня вам не надо ничего делать"
    email.set_content(
        f"""
        <h1>Новая задача</h1>
        {note['note']}
        """,
        subtype="html"
    )
    
    return email