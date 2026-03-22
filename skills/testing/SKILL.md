---
name: testing
description: pytest-bdd setup, BDD step definitions, SQLite test configuration, and async test patterns for FastAPI. Load when writing tests, setting up conftest, or creating BDD scenarios.
allowed-tools: Read, Write, Edit, Bash
---

## Setup

```toml
# pyproject.toml — required, do not change asyncio_mode
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

```bash
uv add --dev pytest pytest-asyncio pytest-bdd pytest-cov httpx aiosqlite
```

## BDD Rules

- Feature files → `tests/bdd/features/` (one per resource)
- Step definitions → `tests/bdd/` (mirror feature file name e.g. `test_auth.py`)
- **Every `.feature` file MUST have a matching step definition file**
- Steps must be **synchronous** — pytest-bdd 8.x does not await async step functions
- Use `sync_client` fixture (`starlette.testclient.TestClient`) for HTTP in steps
- Never rewrite a scenario to match broken behaviour — fix the code

## conftest.py Pattern

```python
# tests/bdd/conftest.py
import pytest
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db.base import Base
from src.main import create_app
from src.api.dependencies import get_db

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   # REQUIRED for SQLite
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
def sync_client(db_engine):
    app = create_app()
    # override get_db with test session bound to db_engine
    with TestClient(app) as client:
        yield client
```

## Known Gotchas

- **pytest-bdd 8.x async (confirmed broken):** Coroutines are not awaited in step functions. All steps MUST be synchronous. `asyncio_mode = "auto"` is still required for async fixtures — do not remove it.
- **`create_all` is mandatory for SQLite:** SQLite starts empty. Always call `await conn.run_sync(Base.metadata.create_all)` in the `db_engine` fixture.
- **SQLite pool config crash:** `pool_size` and `max_overflow` are Postgres-specific. Guard: `if "sqlite" not in str(DATABASE_URL)` before passing to `create_async_engine`.
- **`aiosqlite` must be in dev deps:** `uv add --dev aiosqlite` — without it, SQLite async support silently fails.
- **setuptools, not hatchling:** If using hatchling as build backend, add `[tool.hatch.build.targets.wheel]\npackages = ["src"]` or switch to setuptools to avoid `uv sync` failures.

## Checklist

- [ ] `asyncio_mode = "auto"` in `pyproject.toml`
- [ ] `aiosqlite` in dev dependencies
- [ ] `Base.metadata.create_all` called in `db_engine` fixture
- [ ] SQLite pool config guard in `session.py`
- [ ] Every `.feature` file has a matching step file
- [ ] All step functions are synchronous
- [ ] Coverage ≥ 80% for service layer
