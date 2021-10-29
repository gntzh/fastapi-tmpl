from email.message import EmailMessage
from typing import Any

import aiosmtplib
from jinja2 import Environment, FileSystemLoader

from src.config import settings
from src.infra.security import create_recovery_token, create_verify_email_token

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


async def send_recovery_email(email: str) -> None:
    project_name = settings.PROJECT_NAME
    token = create_recovery_token(email)
    link = f"{settings.RECOVERY_CALLBACK_URL}?token={token}"
    await send_general_email(
        email,
        subject=f"[{project_name}] Recover account",
        title="Recover your account",
        greeting="Hi,",
        message=[f"We got a request to recover your {project_name} account."],
        cta_link=link,
        cta_text="Reset password",
        secondary_message=[
            "If you ignore this message, your password won't be changed.",
            "If you didn't request a password reset, let us know.",
        ],
    )


async def send_verify_email(email: str) -> None:
    project_name = settings.PROJECT_NAME
    token = create_verify_email_token(email)
    link = f"{settings.VERIFY_EMAIL_CALLBACK_URL}?token={token}"
    await send_general_email(
        email,
        subject=f"[{project_name}] Verify Your Email",
        title="Verify your email address",
        greeting="Hi,",
        message=[
            f"To secure your {project_name} account, we just need to "
            f"verify your email address: {email}."
        ],
        cta_link=link,
        cta_text="Verify Email",
        secondary_message=[
            "If you did not request this, you can simply ignore this message."
        ],
    )
