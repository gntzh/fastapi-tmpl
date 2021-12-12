from src.shared.container import Container

from .create_app import create_app

container = Container()
app = create_app(container)
container.wire()
