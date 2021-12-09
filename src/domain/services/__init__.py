from typing import Protocol


class PasswordHashService(Protocol):
    def hash(self, password: str) -> str:
        ...

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        ...


class EmailService(Protocol):
    async def send_welcome_email(self, email: str, name: str) -> None:
        ...

    async def send_verify_email(self, email: str, name: str) -> None:
        ...

    async def send_recovery_email(self, email: str) -> None:
        ...
