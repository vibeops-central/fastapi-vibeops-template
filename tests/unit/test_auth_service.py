import uuid
from unittest.mock import AsyncMock, patch

import pytest

from src.core.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveAccountError,
    InvalidCredentialsError,
)
from src.core.security import hash_password
from src.models.user import User
from src.services.auth_service import AuthService


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def active_user() -> User:
    return User(
        id=uuid.uuid4(),
        email="alice@example.com",
        hashed_password=hash_password("ValidPass1"),
        is_active=True,
    )


@pytest.fixture
def inactive_user() -> User:
    return User(
        id=uuid.uuid4(),
        email="suspended@example.com",
        hashed_password=hash_password("ValidPass1"),
        is_active=False,
    )


class TestAuthServiceRegister:
    async def test_register_new_user_succeeds(self, mock_session, active_user):
        with patch("src.services.auth_service.UserRepository") as MockRepo:
            mock_repo = AsyncMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_by_email.return_value = None
            mock_repo.create.return_value = active_user

            service = AuthService(mock_session)
            result = await service.register("alice@example.com", "ValidPass1")

            assert result == active_user
            mock_repo.get_by_email.assert_called_once_with("alice@example.com")
            mock_repo.create.assert_called_once()

    async def test_register_hashes_password(self, mock_session, active_user):
        with patch("src.services.auth_service.UserRepository") as MockRepo:
            mock_repo = AsyncMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_by_email.return_value = None
            mock_repo.create.return_value = active_user

            service = AuthService(mock_session)
            await service.register("alice@example.com", "ValidPass1")

            _, kwargs = mock_repo.create.call_args
            assert kwargs["hashed_password"] != "ValidPass1"
            assert kwargs["hashed_password"].startswith("$2b$")

    async def test_register_raises_on_duplicate_email(self, mock_session, active_user):
        with patch("src.services.auth_service.UserRepository") as MockRepo:
            mock_repo = AsyncMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_by_email.return_value = active_user

            service = AuthService(mock_session)
            with pytest.raises(EmailAlreadyRegisteredError):
                await service.register("alice@example.com", "ValidPass1")

            mock_repo.create.assert_not_called()


class TestAuthServiceLogin:
    async def test_login_returns_token(self, mock_session, active_user):
        with patch("src.services.auth_service.UserRepository") as MockRepo:
            mock_repo = AsyncMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_by_email.return_value = active_user

            service = AuthService(mock_session)
            token = await service.login("alice@example.com", "ValidPass1")

            assert isinstance(token, str)
            assert len(token) > 0

    async def test_login_raises_on_wrong_password(self, mock_session, active_user):
        with patch("src.services.auth_service.UserRepository") as MockRepo:
            mock_repo = AsyncMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_by_email.return_value = active_user

            service = AuthService(mock_session)
            with pytest.raises(InvalidCredentialsError):
                await service.login("alice@example.com", "wrongpassword")

    async def test_login_raises_on_unknown_email(self, mock_session):
        with patch("src.services.auth_service.UserRepository") as MockRepo:
            mock_repo = AsyncMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_by_email.return_value = None

            service = AuthService(mock_session)
            with pytest.raises(InvalidCredentialsError):
                await service.login("ghost@example.com", "ValidPass1")

    async def test_login_raises_on_inactive_account(self, mock_session, inactive_user):
        with patch("src.services.auth_service.UserRepository") as MockRepo:
            mock_repo = AsyncMock()
            MockRepo.return_value = mock_repo
            mock_repo.get_by_email.return_value = inactive_user

            service = AuthService(mock_session)
            with pytest.raises(InactiveAccountError):
                await service.login("suspended@example.com", "ValidPass1")
