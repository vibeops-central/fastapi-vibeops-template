from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveAccountError,
    InvalidCredentialsError,
)
from src.core.security import create_access_token, hash_password, verify_password
from src.models.user import User
from src.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def register(self, email: str, password: str) -> User:
        existing = await self._repo.get_by_email(email)
        if existing:
            raise EmailAlreadyRegisteredError()
        hashed = hash_password(password)
        return await self._repo.create(email=email, hashed_password=hashed)

    async def login(self, email: str, password: str) -> str:
        user = await self._repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveAccountError()
        return create_access_token(subject=str(user.id))
