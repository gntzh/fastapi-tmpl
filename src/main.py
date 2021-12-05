from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import router
from src.config import settings
from src.infra.db_session import dispose_db

app = FastAPI(title="FastAPI Admin Template")


@app.on_event("shutdown")
async def cleanup_database():
    await dispose_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
