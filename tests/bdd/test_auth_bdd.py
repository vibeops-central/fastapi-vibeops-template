"""
BDD step definitions for auth.feature.

All step functions are synchronous — see tests/bdd/conftest.py for explanation.
Data is passed between steps via target_fixture return values.
"""
import sqlite3

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from starlette.testclient import TestClient

from tests.bdd.conftest import BDD_TEST_DB_PATH

scenarios("features/auth.feature")

VALID_PASSWORD = "ValidPass1"
WEAK_PASSWORD = "short"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _register(client: TestClient, email: str, password: str = VALID_PASSWORD):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )


def _login(client: TestClient, email: str, password: str = VALID_PASSWORD):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('no account exists for "{email}"'))
def no_account_exists(email: str) -> None:
    pass  # clean_bdd_db autouse fixture ensures a fresh state before each test


@given(parsers.parse('an account exists for "{email}" with a known password'), target_fixture="known_user")
def account_exists(sync_client: TestClient, email: str) -> dict:
    _register(sync_client, email, VALID_PASSWORD)
    return {"email": email, "password": VALID_PASSWORD}


@given(parsers.parse('an account already exists for "{email}"'))
def account_already_exists(sync_client: TestClient, email: str) -> None:
    _register(sync_client, email, VALID_PASSWORD)


@given(parsers.parse('an account exists for "{email}" but the account is inactive'), target_fixture="inactive_user_data")
def inactive_account_exists(sync_client: TestClient, email: str) -> dict:
    _register(sync_client, email, VALID_PASSWORD)
    conn = sqlite3.connect(BDD_TEST_DB_PATH)
    conn.execute("UPDATE users SET is_active = 0 WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    return {"email": email, "password": VALID_PASSWORD}


@given(parsers.parse('the user is logged in as "{email}"'), target_fixture="auth_token")
def logged_in_user(sync_client: TestClient, email: str) -> str:
    _register(sync_client, email, VALID_PASSWORD)
    response = _login(sync_client, email, VALID_PASSWORD)
    return response.json()["access_token"]


@given("the user is not logged in")
def not_logged_in() -> None:
    pass


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when(
    parsers.parse('a visitor registers with email "{email}" and a valid password'),
    target_fixture="response",
)
def register_with_valid_password(sync_client: TestClient, email: str):
    return _register(sync_client, email, VALID_PASSWORD)


@when(
    parsers.parse('a visitor tries to register with email "{email}"'),
    target_fixture="response",
)
def register_duplicate(sync_client: TestClient, email: str):
    return _register(sync_client, email, VALID_PASSWORD)


@when(
    parsers.parse('a visitor tries to register with the value "{value}" as their email'),
    target_fixture="response",
)
def register_invalid_email(sync_client: TestClient, value: str):
    return _register(sync_client, value, VALID_PASSWORD)


@when(
    parsers.parse('a visitor tries to register with email "{email}" and a password that is too short'),
    target_fixture="response",
)
def register_weak_password(sync_client: TestClient, email: str):
    return _register(sync_client, email, WEAK_PASSWORD)


@when(
    parsers.parse('the user logs in with email "{email}" and the correct password'),
    target_fixture="response",
)
def login_correct(sync_client: TestClient, email: str):
    return _login(sync_client, email, VALID_PASSWORD)


@when(
    parsers.parse('the user tries to log in with email "{email}" and an incorrect password'),
    target_fixture="response",
)
def login_wrong_password(sync_client: TestClient, email: str):
    return _login(sync_client, email, "WrongPass1")


@when(
    parsers.parse('the user tries to log in with email "{email}"'),
    target_fixture="response",
)
def login_unknown_email(sync_client: TestClient, email: str):
    return _login(sync_client, email, VALID_PASSWORD)


@when(
    parsers.parse('the user tries to log in with email "{email}" and the correct password'),
    target_fixture="response",
)
def login_inactive_account(sync_client: TestClient, email: str):
    return _login(sync_client, email, VALID_PASSWORD)


@when("the user requests their profile", target_fixture="response")
def get_profile(sync_client: TestClient, auth_token: str):
    return sync_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {auth_token}"},
    )


@when("the user attempts to access a protected resource", target_fixture="response")
def access_protected_unauthenticated(sync_client: TestClient):
    return sync_client.get("/api/v1/auth/me")


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("a new account is created")
def account_created(response) -> None:
    assert response.status_code == 201


@then("the response includes the account email and a unique identifier")
def response_has_email_and_id(response) -> None:
    data = response.json()
    assert "email" in data
    assert "id" in data


@then("the response contains the account email and identifier")
def response_contains_email_and_id(response) -> None:
    data = response.json()
    assert "email" in data
    assert "id" in data


@then("no password or credential is included in the response")
def no_password_in_response(response) -> None:
    data = response.json()
    assert "password" not in data
    assert "hashed_password" not in data
    assert "access_token" not in data


@then("registration is rejected")
def registration_rejected(response) -> None:
    assert response.status_code in (409, 422)


@then("the visitor is told the email address is already taken")
def told_email_taken(response) -> None:
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]


@then("the visitor is told to provide a valid email address")
def told_invalid_email(response) -> None:
    assert response.status_code == 422


@then("the visitor is told the password does not meet the requirements")
def told_weak_password(response) -> None:
    assert response.status_code == 422


@then("login succeeds")
def login_succeeds(response) -> None:
    assert response.status_code == 200


@then("the response contains an access token")
def response_has_token(response) -> None:
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@then("login is rejected")
def login_rejected(response) -> None:
    assert response.status_code in (401, 403)


@then("the user receives a generic invalid credentials message")
def generic_credentials_message(response) -> None:
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@then("the user is told the account is not active")
def told_inactive(response) -> None:
    assert response.status_code == 403
    assert response.json()["detail"] == "Account is not active"


@then("the request is rejected")
def request_rejected(response) -> None:
    assert response.status_code in (401, 403)


@then("the user is told authentication is required")
def told_auth_required(response) -> None:
    assert response.status_code in (401, 403)
