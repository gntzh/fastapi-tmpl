import sys

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from src.api.router import router
from src.config import settings
from src.infra.db_session import dispose_db
from src.shared.container import Container

loggin_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "level": settings.LOGGING_LEVEL,
        }
    ]
}
logger.configure(**loggin_config)


container = Container()
container.wire()

app = FastAPI(title="FastAPI Admin Template")
app.include_router(router)


@app.on_event("shutdown")
async def cleanup_database():
    await dispose_db()
    await container.db().dispose_db()


@app.middleware("http")
async def shutdown_request_scope_resources(request: Request, call_next):
    res = await call_next(request)
    if (awaitable := container.session.shutdown()) is not None:
        await awaitable
    return res


sentry_sdk.init(settings.SENTRY_DSN)
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
