import sys

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from src.api.router import router
from src.config import settings
from src.shared.container import Container


def create_app(container: Container) -> FastAPI:
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
    app.include_router(router)

    @app.on_event("shutdown")
    async def cleanup_database():
        await container.db().dispose_db()

    @app.middleware("http")
    async def shutdown_request_scope_resources(request: Request, call_next):
        res = await call_next(request)
        logger.debug("middleware will shutdown session")
        if (awaitable := container.session.shutdown()) is not None:
            logger.debug("middleware shutdowned session")
            await awaitable
        else:
            logger.debug("middleware have not init")
        return res

    sentry_sdk.init(settings.SENTRY_DSN)
    app.add_middleware(SentryAsgiMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
