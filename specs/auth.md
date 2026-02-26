# Technical Design: User Authentication

**Feature:** User registration and login with email and password
**Status:** Awaiting approval
**Date:** 2026-02-26

---

## 1. Overview

Allow users to create an account with an email and password, and authenticate to receive a JWT access token for use with protected endpoints.

---

## 2. Data Model

### Table: `users`

| Column             | Type         | Constraints                        |
|--------------------|--------------|------------------------------------|
| `id`               | UUID         | PK, default gen_random_uuid()      |
| `email`            | VARCHAR(255) | UNIQUE, NOT NULL, indexed          |
| `hashed_password`  | VARCHAR(255) | NOT NULL                           |
| `is_active`        | BOOLEAN      | NOT NULL, default TRUE             |
| `created_at`       | TIMESTAMPTZ  | NOT NULL, default now()            |
| `updated_at`       | TIMESTAMPTZ  | NOT NULL, default now(), on update |

**Notes:**
- `email` is lowercased and stripped before storage
- `hashed_password` stores the bcrypt hash only — the plaintext password is never persisted
- `is_active` allows soft-disabling accounts without deletion

---

## 3. API Endpoints

### POST `/api/v1/auth/register`
- **Auth required:** No (explicitly public)
- **Request body:** `email`, `password`
- **Response (201):** `id`, `email`, `is_active`, `created_at`
- **Errors:**
  - `409 Conflict` — email already registered
  - `422 Unprocessable Entity` — validation failure (invalid email format, password too short)

### POST `/api/v1/auth/login`
- **Auth required:** No (explicitly public)
- **Request body:** `email`, `password`
- **Response (200):** `access_token`, `token_type`
- **Errors:**
  - `401 Unauthorized` — invalid credentials (email not found or password mismatch)
  - `403 Forbidden` — account is inactive

### GET `/api/v1/auth/me`
- **Auth required:** Yes (JWT Bearer token)
- **Response (200):** `id`, `email`, `is_active`, `created_at`
- **Errors:**
  - `401 Unauthorized` — missing or invalid token

---

## 4. Pydantic Schemas

| Schema              | Purpose                                      |
|---------------------|----------------------------------------------|
| `RegisterRequest`   | Validates registration input                 |
| `LoginRequest`      | Validates login input                        |
| `TokenResponse`     | Access token response                        |
| `UserResponse`      | Public user representation (no password)     |

**Password validation rules (enforced in `RegisterRequest`):**
- Minimum 8 characters
- At least one uppercase letter
- At least one digit

---

## 5. Service Layer: `AuthService`

| Method                                   | Responsibility                                      |
|------------------------------------------|-----------------------------------------------------|
| `register(email, password) → User`       | Check uniqueness, hash password, persist user       |
| `login(email, password) → str`           | Verify credentials, issue JWT access token          |
| `get_current_user(token) → User`         | Decode JWT, load user from DB                       |

---

## 6. Repository Layer: `UserRepository`

| Method                                      | Responsibility                   |
|---------------------------------------------|----------------------------------|
| `get_by_email(email) → User | None`          | Lookup user by email             |
| `get_by_id(id) → User | None`               | Lookup user by UUID              |
| `create(email, hashed_password) → User`     | Insert new user row              |

---

## 7. Security Considerations

- **Password hashing:** `bcrypt.hashpw` / `bcrypt.checkpw` — no `passlib` (incompatible with bcrypt 4.x+)
- **JWT secret:** Loaded from `SECRET_KEY` environment variable via Pydantic Settings — never hardcoded
- **Token expiry:** Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in settings (default: 30)
- **Algorithm:** HS256
- **Passwords never logged:** Log output must never include raw passwords or tokens
- **Error messages:** Login failures return a generic "invalid credentials" message — do not distinguish between "email not found" and "wrong password" to prevent user enumeration
- **Inactive accounts:** Blocked at login — they receive a 403, not a 401, to distinguish the failure mode

---

## 8. Architectural Decisions

- **No refresh tokens in v1:** Keeping scope minimal — access tokens only. Refresh token support is a future ADR candidate.
- **Email normalisation:** Emails are lowercased on input in the service layer before any DB interaction.
- **No email verification in v1:** Account activation via email link is out of scope for this feature. `is_active` defaults to `TRUE` on registration.
- **JWT dependency:** A shared `get_current_user` dependency in `src/api/dependencies.py` is used across all authenticated endpoints — not re-implemented per route.

---

## 9. File Locations

```
src/
├── api/v1/endpoints/auth.py       # Route handlers
├── api/v1/router.py               # Register auth router
├── api/dependencies.py            # get_current_user dependency
├── core/
│   ├── config.py                  # Add ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
│   └── security.py                # JWT encode/decode, bcrypt helpers
├── models/user.py                 # User SQLAlchemy model
├── schemas/auth.py                # RegisterRequest, LoginRequest, TokenResponse, UserResponse
├── services/auth_service.py       # AuthService
└── repositories/user_repository.py  # UserRepository

alembic/versions/
└── xxxx_create_users_table.py     # Migration

tests/
├── unit/test_auth_service.py
├── integration/test_auth_endpoints.py
└── bdd/
    ├── features/auth.feature
    └── test_auth_bdd.py
```
