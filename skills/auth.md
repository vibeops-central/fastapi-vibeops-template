# Skill: Authentication & Security

> Load this skill when implementing: JWT auth, user registration/login, password handling, token refresh, protected endpoints.

---

## Patterns

- Use **bcrypt directly** (`bcrypt.hashpw` / `bcrypt.checkpw`) — do NOT use passlib (incompatible with bcrypt 4.x+)
- JWT: short-lived access tokens (1h) + long-lived refresh tokens (7d)
- `SECRET_KEY` must be ≥ 32 characters — enforce in Pydantic Settings validator
- Never log or return password hashes — ever
- Use `HTTPBearer` dependency for protected endpoints

## Status Codes

| Situation | Code |
|-----------|------|
| Pydantic validation failure (invalid email, weak password) | `422` |
| Business rule rejection (duplicate email) | `400` |
| Missing or invalid/expired token | `401` |
| Valid token but insufficient permissions | `403` |
| Resource conflict | `409` |

> Do not conflate 422 (schema) with 400 (business logic), or 401 (no auth) with 403 (wrong auth).

## Dependencies

When adding auth to a project, always include:
```
uv add 'pydantic[email]'     # required for EmailStr — plain pydantic does NOT bundle email-validator
uv add bcrypt
uv add python-jose[cryptography]
```

## Known Gotchas

- **passlib incompatibility:** `passlib 1.7.4` removed `__about__` in bcrypt 4.x+. Use bcrypt directly.
- **`pydantic[email]` is not optional:** `EmailStr` silently fails at import if `email-validator` is missing. Always use `pydantic[email]`, not `pydantic`.
- **401 vs 403:** FastAPI's `HTTPBearer` returns `401` for missing/invalid tokens. `403` is for authenticated users who lack permission. Steps and assertions must reflect this.

## Checklist (append to self-review)

- [ ] `pydantic[email]` added to `pyproject.toml`
- [ ] bcrypt used directly — no passlib
- [ ] `SECRET_KEY` validated as ≥ 32 chars in Settings
- [ ] No password hashes in logs or API responses
- [ ] 422 / 400 / 401 / 403 used correctly (see table above)
- [ ] Token expiry tested in Gherkin scenarios
