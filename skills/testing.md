# Skill: Testing

> Load this skill when: writing tests, setting up conftest, writing BDD step definitions, or running pytest.

---

## Setup

### pyproject.toml (required)
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"    # do NOT change this — required for async fixtures
```

### Dev dependencies
```
uv add --dev pytest pytest-asyncio pytest-bdd pytest-cov httpx aiosqlite
```

## BDD Rules

- Feature files → `tests/bdd/features/` (one per resource)
- Step definitions → `tests/bdd/` (mirror feature file name)
- **Every `.feature` file MUST have a matching step definition file** — the feature file alone is not runnable
- Steps must be **synchronous** — pytest-bdd 8.x does not await async step functions
- Use `sync_client` fixture (`starlette.testclient.TestClient`) for HTTP calls in steps
- Never rewrite a scenario to match broken behaviour — fix the code

## conftest.py Pattern (SQLite for tests)

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

@pytest.fixture(scope="session")
def event_loop_policy():
    import asyncio
    return asyncio.DefaultEventLoopPolicy()

@pytest.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   # ← REQUIRED for SQLite
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
def sync_client(db_engine):
    # ... override get_db dependency with test engine
    app = create_app()
    with TestClient(app) as client:
        yield client
```

## Known Gotchas

- **pytest-bdd 8.x async (confirmed broken):** Coroutines passed to step functions are not awaited. All step functions MUST be synchronous. `asyncio_mode = "auto"` is still required for async fixtures — do not remove it.
- **`create_all` is mandatory for SQLite:** SQLite starts empty. Always call `await conn.run_sync(Base.metadata.create_all)` in the `db_engine` fixture. Postgres uses Alembic migrations instead.
- **SQLite pool config crash:** `pool_size` and `max_overflow` are Postgres-specific. Guard them: `if "sqlite" not in str(DATABASE_URL)` before passing to `create_async_engine`.
- **`aiosqlite` must be installed:** Add `uv add --dev aiosqlite` for SQLite async support in tests.
- **Status code expectations:** See `skills/auth.md` for 422 / 400 / 401 / 403 rules.

## Checklist (append to self-review)

- [ ] `asyncio_mode = "auto"` in `pyproject.toml`
- [ ] `aiosqlite` in dev dependencies
- [ ] `Base.metadata.create_all` called in `db_engine` fixture
- [ ] SQLite pool config guard in `session.py`
- [ ] Every `.feature` file has a matching step file
- [ ] All step functions are synchronous (not async)
- [ ] No existing tests deleted or skipped
- [ ] Coverage ≥ 80% for service layer
