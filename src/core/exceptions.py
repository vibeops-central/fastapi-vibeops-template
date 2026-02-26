from fastapi import Request
from fastapi.responses import JSONResponse


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InactiveAccountError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


async def email_already_registered_handler(
    request: Request, exc: EmailAlreadyRegisteredError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Email address is already registered"},
    )


async def invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid credentials"},
    )


async def inactive_account_handler(
    request: Request, exc: InactiveAccountError
) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"detail": "Account is not active"},
    )
