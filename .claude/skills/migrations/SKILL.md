---
name: migrations
description: Alembic async migration setup, schema change rules, and SQLAlchemy 2.0 model patterns for FastAPI. Load when adding or modifying database models or running migrations.
allowed-tools: Read, Write, Edit, Bash(alembic:*)
---

## Rules

- **All schema changes via Alembic** — never alter the DB schema manually
- **Always review autogenerate output** before applying — it misses RLS policies, custom types, partial indexes
- Use **async migration setup** in `alembic/env.py` — do not replace with sync version
- Use `Mapped[]` and `mapped_column()` for all model columns (SQLAlchemy 2.0)
- Use `select()` style queries — not legacy `session.query()`

## Async env.py Pattern

```python
# alembic/env.py — async setup, do not change to sync
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.db.base import Base

target_metadata = Base.metadata

def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
    )
    # use asyncio.run() with async migration runner
```

## Known Gotchas

- **Alembic + async:** Default template is synchronous — always use the async setup.
- **autogenerate limitations:** Does not detect renamed columns (sees drop + add), CHECK constraints, RLS policies. Always review the diff.
- **Session scope:** The DB session dependency uses `yield` — do not close it manually inside services or it breaks the request lifecycle.

## Checklist

- [ ] Alembic migration generated and reviewed if schema changed
- [ ] Async `env.py` preserved
- [ ] `Mapped[]` / `mapped_column()` used for all new columns
- [ ] No manual schema changes
