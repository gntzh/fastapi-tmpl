from fastapi import FastAPI

from src.infra.db_session import engine
from src.api.router import router

app = FastAPI(title="FastAPI Admin Template")

app.on_event("on")


@app.on_event("shutdown")
async def cleanup_database():
    print("dispose")
    await engine.dispose()


app.include_router(router)
