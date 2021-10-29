from email.message import EmailMessage
from typing import Any

import aiosmtplib
from jinja2 import Environment, FileSystemLoader

from src.config import settings

env = Environment(
    loader=FileSystemLoader(settings.BASE_DIR / "src/templates/email"), autoescape=True
)


async def send_general_email(
    to: Any,
    subject: str,
    title: str,
    message: list[str],
    greeting: str = None,
    cta_text: str = None,
    cta_link: str = None,
    secondary_message: list[str] = None,
) -> None:
    context = {
        "project_name": settings.PROJECT_NAME,
        "title": title,
        "greeting": greeting,
        "cta_text": cta_text,
        "cta_link": cta_link,
        "message": message,
        "secondary_message": secondary_message,
    }
    text = env.get_template("general.txt").render(context)
    html = env.get_template("general.html").render(context)
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = str(settings.EMAIL_DEFAULT_FROM)
    msg["To"] = to
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")
    await aiosmtplib.send(
        msg,
        hostname=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_USERNAME,
        password=settings.EMAIL_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
        start_tls=settings.EMAIL_USE_STARTTLS,
    )
