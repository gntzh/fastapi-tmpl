from email.message import EmailMessage

from anyio import sleep


class EmailSenderInMemory:
    outbox: list[EmailMessage]

    def __init__(self) -> None:
        self.outbox = []

    async def send(self, message: EmailMessage):
        await sleep(2)
        self.outbox.append(message)
