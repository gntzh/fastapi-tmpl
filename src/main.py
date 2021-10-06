from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import router
from src.config import settings
from src.infra.db_session import engine

app = FastAPI(title="FastAPI Admin Template")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def cleanup_database():
    print("dispose")
    await engine.dispose()


app.include_router(router)
