import sys

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from src.api.router import router
from src.config import settings
from src.infra.db_session import dispose_db

loggin_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "level": settings.LOGGING_LEVEL,
        }
    ]
}
logger.configure(**loggin_config)


app = FastAPI(title="FastAPI Admin Template")


@app.on_event("shutdown")
async def cleanup_database():
    await dispose_db()


sentry_sdk.init(settings.SENTRY_DSN)
app.add_middleware(SentryAsgiMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
