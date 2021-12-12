from email.message import EmailMessage
from typing import Any, Protocol

import aiosmtplib
from dependency_injector.wiring import Provide
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from src.config import settings

env = Environment(
    loader=FileSystemLoader(settings.BASE_DIR / "src/templates/email"), autoescape=True
)

PROJECT_NAME: str = Provide["config.PROJECT_NAME"]


class EmailSender(Protocol):
    async def send(self, message: EmailMessage) -> Any:
        ...


class SMTPEmailSender:
    def __init__(
        self,
        hostname: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool,
        start_tls: bool,
    ) -> None:
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.start_tls = start_tls

    async def send(self, message: "EmailMessage"):
        return await aiosmtplib.send(
            message,
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=self.use_tls,
            start_tls=self.start_tls,
        )


class EmailService:
    def __init__(self, email_sender: EmailSender) -> None:
        self.email_sender = email_sender

    async def send_general_email(
        self,
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
        res = await self.email_sender.send(msg)
        logger.info("send email result: {}", res)

    async def send_recovery_email(self, email: str, token: str) -> None:
        project_name = settings.PROJECT_NAME
        link = f"{settings.RECOVERY_CALLBACK_URL}?token={token}"
        await self.send_general_email(
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

    async def send_verify_email(self, email: str, name: str, token: str) -> None:
        project_name = settings.PROJECT_NAME
        link = f"{settings.VERIFY_EMAIL_CALLBACK_URL}?token={token}"
        await self.send_general_email(
            f"{name} <{email}>",
            subject=f"[{project_name}] Verify Your Email",
            title="Verify your email address",
            greeting=f"Hi, {name}",
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

    async def send_welcome_email(self, email: str, name: str, token: str) -> None:
        project_name = settings.PROJECT_NAME
        link = f"{settings.VERIFY_EMAIL_CALLBACK_URL}?token={token}"
        title = f"Welcome to {project_name}"
        await self.send_general_email(
            f"{name} <{email}>",
            subject=title,
            title=title,
            greeting=f"Hi, {name}",
            message=[
                f"Thanks for signing up to {project_name}! "
                f"Please also take a moment to verify your email address: {email}."
            ],
            cta_link=link,
            cta_text="Verify Email",
            secondary_message=[
                "If you did not request this, you can simply ignore this message."
            ],
        )
