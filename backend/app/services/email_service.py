import smtplib
from email.message import EmailMessage

from flask import current_app


def send_email(to_email: str, subject: str, text: str) -> bool:
    host = current_app.config["SMTP_HOST"]
    username = current_app.config["SMTP_USERNAME"]
    password = current_app.config["SMTP_PASSWORD"]
    from_email = current_app.config["EMAIL_FROM"] or username
    if not all([host, username, password, from_email]):
        current_app.logger.warning("Email skipped because SMTP is not configured")
        return False

    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(text)

    with smtplib.SMTP(host, current_app.config["SMTP_PORT"]) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)
    return True

