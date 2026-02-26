from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="FastAPI VibeOps Template",
    description="A reference implementation of a VibeOps-primed FastAPI environment.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(users.router)


@app.get("/healthz", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
