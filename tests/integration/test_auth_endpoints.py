import pytest
from httpx import AsyncClient


class TestRegisterEndpoint:
    async def test_register_success(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "alice@example.com", "password": "ValidPass1"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "alice@example.com"
        assert "id" in data
        assert data["is_active"] is True
        assert "password" not in data
        assert "hashed_password" not in data

    async def test_register_duplicate_email_returns_409(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={"email": "bob@example.com", "password": "ValidPass1"},
        )
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "bob@example.com", "password": "ValidPass1"},
        )
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]

    async def test_register_invalid_email_returns_422(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "ValidPass1"},
        )
        assert response.status_code == 422

    async def test_register_weak_password_returns_422(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "carol@example.com", "password": "short"},
        )
        assert response.status_code == 422

    async def test_register_password_missing_uppercase_returns_422(
        self, client: AsyncClient
    ):
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "carol@example.com", "password": "alllowercase1"},
        )
        assert response.status_code == 422

    async def test_register_password_missing_digit_returns_422(
        self, client: AsyncClient
    ):
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "carol@example.com", "password": "NoDigitsHere"},
        )
        assert response.status_code == 422


class TestLoginEndpoint:
    async def test_login_success(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={"email": "dave@example.com", "password": "ValidPass1"},
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "dave@example.com", "password": "ValidPass1"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password_returns_401(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={"email": "eve@example.com", "password": "ValidPass1"},
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "eve@example.com", "password": "WrongPass1"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    async def test_login_unknown_email_returns_401(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "ghost@example.com", "password": "ValidPass1"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    async def test_login_does_not_reveal_whether_email_exists(
        self, client: AsyncClient
    ):
        # Wrong password for existing user and unknown email return identical responses
        await client.post(
            "/api/v1/auth/register",
            json={"email": "frank@example.com", "password": "ValidPass1"},
        )
        wrong_pass_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "frank@example.com", "password": "WrongPass1"},
        )
        unknown_email_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@example.com", "password": "ValidPass1"},
        )
        assert wrong_pass_response.status_code == unknown_email_response.status_code
        assert wrong_pass_response.json() == unknown_email_response.json()


class TestMeEndpoint:
    async def test_me_returns_current_user(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={"email": "grace@example.com", "password": "ValidPass1"},
        )
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "grace@example.com", "password": "ValidPass1"},
        )
        token = login_response.json()["access_token"]

        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "grace@example.com"
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data

    async def test_me_without_token_returns_401(self, client: AsyncClient):
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    async def test_me_with_invalid_token_returns_401(self, client: AsyncClient):
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer notavalidtoken"},
        )
        assert response.status_code == 401
