# Skill: Database Migrations (Alembic)

> Load this skill when: adding/modifying models, running migrations, or setting up Alembic for the first time.

---

## Rules

- **All schema changes via Alembic** — never alter the DB schema manually
- **Always review autogenerate output** before applying — `--autogenerate` misses things (RLS policies, custom types, partial indexes)
- Use **async migration setup** in `alembic/env.py` — do not replace with sync version
- Never run `alembic upgrade head` in production without reviewing the migration script first
- Use `Mapped[]` and `mapped_column()` for all model columns (SQLAlchemy 2.0 style)
- Use `select()` style queries — not legacy `session.query()`

## Async env.py Pattern

```python
# alembic/env.py (async setup — do not change to sync)
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.db.base import Base

target_metadata = Base.metadata

def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
    )
    # ... async migration runner
```

## Known Gotchas

- **Alembic + async:** Default Alembic template is synchronous — always use the async setup. Do not revert to sync `engine_from_config`.
- **autogenerate limitations:** Does not detect: renamed columns (sees drop + add), custom CHECK constraints, RLS policies. Always review the diff before applying.
- **Session scope:** The DB session dependency uses `yield` — do not close it manually inside services or it breaks the request lifecycle.

## Checklist (append to self-review)

- [ ] Alembic migration generated if schema changed
- [ ] Migration script reviewed before applying
- [ ] Async `env.py` setup preserved
- [ ] `Mapped[]` / `mapped_column()` used for all new columns
