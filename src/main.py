from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.router import v1_router
from src.core.config import settings
from src.core.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveAccountError,
    InvalidCredentialsError,
    email_already_registered_handler,
    inactive_account_handler,
    invalid_credentials_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown


app = FastAPI(title="FastAPI VibeOps Template", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(EmailAlreadyRegisteredError, email_already_registered_handler)  # type: ignore[arg-type]
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)  # type: ignore[arg-type]
app.add_exception_handler(InactiveAccountError, inactive_account_handler)  # type: ignore[arg-type]

app.include_router(v1_router)
