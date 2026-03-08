# AGENTS.md — fastapi-vibeops-template
> This is a living document — agents are expected to propose updates, not just follow rules.
> Every correction, discovery, or new pattern is a candidate for inclusion.
> Propose → Get approval → Update file → Log the change.
>
> Repo: https://github.com/natulauchande/fastapi-vibeops-template
> Framework: https://github.com/natulauchande/vibeops
>
> Note: CLAUDE.md is a symlink to this file for Claude Code compatibility.
> This file is agent-agnostic and works with any coding agent.
>
> Skills loaded alongside this file:
> - vibeops-skill  → universal VibeOps methodology (workflows, protocols, evaluation)

---

## 1. Project Overview

**Repo:** fastapi-vibeops-template
**Stack:** Python 3.11 / FastAPI / PostgreSQL / SQLAlchemy 2.0 / Alembic / Redis / Docker
**Purpose:** A VibeOps-primed FastAPI project template. AI agents operating in this repo work within
defined guardrails — configuration-driven, spec-first, test-protected, and compliance-aware.

---

## 2. Build & Environment

### Package Manager
This project uses **`uv`** for dependency management — NOT pip directly.

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package>              # production dependency
uv add --dev <package>        # dev/test dependency

# Run the app (local dev)
uv run uvicorn src.main:app --reload --port 8000

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run BDD tests only
uv run pytest tests/bdd/

# Lint and format
uv run ruff check .
uv run ruff format .

# Type checking
uv run mypy src/

# Vibecheck Score
uv run vibecheck .
```

### Environment Setup
- Copy `.env.example` to `.env` and populate all required values
- Never commit `.env` — it is gitignored
- Use `python-dotenv` for local dev; in production, secrets are injected via environment variables
- Required variables: `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `ALLOWED_ORIGINS`

---

## 3. Repository Structure

```
/
├── src/
│   ├── main.py               # FastAPI app factory and lifespan events
│   ├── api/
│   │   ├── v1/               # API version 1 routes
│   │   │   ├── endpoints/    # One file per resource (users.py, items.py)
│   │   │   └── router.py     # Aggregates all v1 routers
│   │   └── dependencies.py   # Shared FastAPI dependencies (auth, db session)
│   ├── core/
│   │   ├── config.py         # Pydantic Settings — all config lives here
│   │   ├── security.py       # JWT, password hashing, token utilities
│   │   └── exceptions.py     # Custom exception classes and handlers
│   ├── models/               # SQLAlchemy ORM models
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # Business logic — all domain logic lives here
│   ├── repositories/         # Data access layer — DB queries only, no logic
│   └── db/
│       ├── session.py        # Async SQLAlchemy session factory
│       └── base.py           # Base model class
├── alembic/                  # Database migrations
│   └── versions/
├── tests/
│   ├── conftest.py           # Pytest fixtures (test client, test DB)
│   ├── unit/                 # Unit tests for services and utilities
│   ├── integration/          # Integration tests for API endpoints
│   └── bdd/                  # BDD step definitions (mirrors features/)
│       └── features/         # Gherkin feature files — one per resource
├── specs/
│   ├── adr/                  # Architecture Decision Records
│   └── openapi.yaml          # API contract (auto-generated or hand-authored)
├── .claude/
│   └── skills/
│       └── vibeops-skill/    # VibeOps universal methodology skill
│           └── SKILL.md
├── vibecheck/                # Vibecheck Score computation library
├── experiments/              # MLflow experiment configs and results
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── Makefile                  # setup, test, lint, vibecheck targets
├── AGENTS.md                 # You are here (primary file)
├── CLAUDE.md                 # Symlink → AGENTS.md (Claude Code compatibility)
└── LICENSE                   # MIT
```

---

## 4. Architecture & Design Patterns

### Layered Architecture (strictly enforced)
```
Request → Router → Dependency → Service → Repository → Database
```
- **Routers** handle HTTP only — no business logic, no direct DB access
- **Services** own all business logic — call repositories, not models directly
- **Repositories** handle all DB queries — return domain objects, not raw rows
- **Schemas** (Pydantic) handle all request validation and response serialization
- **Models** (SQLAlchemy) represent DB tables only — no business logic on models

### FastAPI Specific Conventions
- Use **async/await** throughout — no synchronous DB calls in async endpoints
- Use **dependency injection** for database sessions, authentication, and shared resources
- All endpoints must declare explicit **response_model** — never return raw dicts
- Use **APIRouter** with prefix and tags for every resource — never define routes on the app directly
- Use **Pydantic Settings** (`src/core/config.py`) for all configuration — no hardcoded values anywhere
- Background tasks use **FastAPI BackgroundTasks** for lightweight jobs, **Celery** for heavy/scheduled work
- Use **lifespan context manager** in `main.py` for startup/shutdown events — not deprecated `@app.on_event`

### Database
- Use **async SQLAlchemy 2.0** syntax (`async with session` / `await session.execute`)
- All migrations via **Alembic** — never alter the DB schema manually
- Always use **`select()`** style queries (SQLAlchemy 2.0) — not legacy `session.query()`
- Use **`Mapped[]`** and `mapped_column()` for model column definitions
- Database sessions are injected via dependency — never instantiate sessions inside services

### Error Handling
- Define custom exceptions in `src/core/exceptions.py`
- Register global exception handlers in `main.py`
- Never expose internal error details to API consumers — return sanitized messages
- Use appropriate HTTP status codes — do not return 200 for errors

---

## 5. Hard Constraints (Non-Negotiables)

- **Authentication:** All endpoints are authenticated by default via JWT dependency. Unauthenticated endpoints must be explicitly marked and approved.
- **Authorization:** Role-based access is enforced at the service layer — never trust client-supplied roles.
- **Secrets:** No secrets, API keys, or credentials in source code or committed files — ever.
- **PII / Sensitive Data:** Never log passwords, tokens, ID numbers, or financial data. Mask in all log output.
- **Input Validation:** All inputs validated via Pydantic schemas before reaching the service layer — no raw request data in services.
- **Dependencies:** Do not add new packages without flagging first — ask for approval before running `uv add`.
- **Breaking Changes:** Do not modify existing API response schemas without versioning — add a new schema, deprecate the old one.
- **Migrations:** Never use `--autogenerate` alone without reviewing the generated migration script before applying.
- **Spec Gate:** A spec without Gherkin is incomplete. A Gherkin scenario without a passing test is a lie. Both must exist before a feature is merged.
- **Compliance behaviours** (auth, data access, audit trails) MUST have a corresponding Gherkin scenario — no exceptions.

---

## 6. Testing Rules

- **Never delete, skip, or modify existing tests** to make them pass — this is a critical violation
- All new endpoints must have integration tests in `tests/integration/`
- All new service methods must have unit tests in `tests/unit/`
- Use **pytest-asyncio** for async test functions (`asyncio_mode = "auto"` in `pyproject.toml`)
- Use **httpx.AsyncClient** for async endpoint tests
- Use **factory_boy** or fixtures for test data — no hardcoded test values
- Mock external services — never call real services in tests
- Minimum coverage target: **80%** for the service layer

---

## 7. Known Gotchas & Tribal Knowledge

- **Session scope:** The DB session dependency uses `yield` — do not close it manually inside services
- **Async pitfall:** Do not use `time.sleep()` in async code — use `await asyncio.sleep()` instead
- **Alembic + async:** Use the async migration setup in `alembic/env.py`, do not replace it
- **CORS:** `ALLOWED_ORIGINS` must be set explicitly in production — wildcard `*` is only permitted in local dev
- **Pydantic v2:** Use `model_validate()` not `parse_obj()`, and `model_dump()` not `dict()`
- **Redis cache:** Cache keys follow the pattern `{resource}:{id}:{version}` — do not invent new patterns
- **pytest-bdd async (confirmed broken in 8.x):** All BDD step functions must be **synchronous**. Use the `sync_client` fixture (`starlette.testclient.TestClient`) in `tests/bdd/conftest.py`. `asyncio_mode = "auto"` is still required — do not remove it.
- **passlib + bcrypt incompatibility:** Do not add `passlib` — use `bcrypt` directly (`bcrypt.hashpw` / `bcrypt.checkpw`)
- **Symlink:** CLAUDE.md is a symlink to this file — always edit AGENTS.md, never CLAUDE.md directly

---

## 8. Change Log

| Date       | Change                                                                        | Author         |
|------------|-------------------------------------------------------------------------------|----------------|
| 2025-01-01 | Initial AGENTS.md created                                                     | Natu Lauchande |
| 2025-01-15 | Added async SQLAlchemy 2.0 conventions                                        | Natu Lauchande |
| 2025-02-01 | Added BDD/Gherkin rules and spec-first workflow                               | Natu Lauchande |
| 2025-02-20 | Added VibeOps principles section                                              | Natu Lauchande |
| 2025-02-20 | Added self-updating protocol                                                  | Natu Lauchande |
| 2025-02-21 | Renamed primary file from CLAUDE.md to AGENTS.md                              | Natu Lauchande |
| 2025-02-21 | CLAUDE.md is now a symlink to AGENTS.md                                       | Natu Lauchande |
| 2025-02-21 | Added spec types table and dual-spec rule                                     | Natu Lauchande |
| 2025-02-21 | Replaced feature kickoff prompt with auto protocol                            | Natu Lauchande |
| 2026-02-21 | Corrected BDD client rule: steps must use sync_client                         | Claude         |
| 2026-02-21 | Added pytest-bdd 8.x async gotcha with full workaround                        | Claude         |
| 2026-02-21 | Added passlib/bcrypt incompatibility gotcha                                   | Claude         |
| 2026-03-08 | Extracted methodology → .claude/skills/vibeops-skill; AGENTS.md is config only | Claude       |
