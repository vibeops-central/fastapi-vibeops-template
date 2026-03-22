# AGENTS.md — fastapi-vibeops-template
> This is a living document — agents are expected to propose updates, not just follow rules.
> Every correction, discovery, or new pattern is a candidate for inclusion.
> Propose → Get approval → Update file → Log the change.
>
> Repo: https://github.com/vibeops-central/fastapi-vibeops-template
> Framework: https://github.com/vibeops-central/vibeops
>
> Note: CLAUDE.md is a symlink to this file for Claude Code compatibility.
> This file is agent-agnostic and works with any coding agent.

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
uv sync                                          # install dependencies
uv add <package>                                 # production dependency
uv add --dev <package>                           # dev/test dependency
uv run uvicorn src.main:app --reload --port 8000 # run app
uv run pytest                                    # run tests
uv run pytest --cov=src --cov-report=term-missing
uv run pytest tests/bdd/                         # BDD only
uv run ruff check . && uv run ruff format .      # lint + format
uv run mypy src/                                 # type check
uv run vibecheck .                               # VibeOps score
```

### Environment Setup
- Copy `.env.example` to `.env` and populate all required values
- Never commit `.env` — it is gitignored
- Required variables: `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `ALLOWED_ORIGINS`

---

## 3. Repository Structure

```
/
├── src/
│   ├── main.py               # FastAPI app factory and lifespan events
│   ├── api/v1/endpoints/     # One file per resource
│   ├── core/                 # config.py, security.py, exceptions.py
│   ├── models/               # SQLAlchemy ORM models
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # Business logic
│   ├── repositories/         # Data access layer
│   └── db/                   # session.py, base.py
├── alembic/versions/
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── bdd/features/
├── specs/
├── skills/                   # ← Governance skill modules (load as needed)
├── experiments/              # ← Experiment docs and results
├── vibecheck/
├── AGENTS.md                 # You are here
└── CLAUDE.md                 # Symlink → AGENTS.md
```

---

## 4. Architecture & Design Patterns

```
Request → Router → Dependency → Service → Repository → Database
```

- **Routers** — HTTP only, no business logic, no direct DB access
- **Services** — all business logic, call repositories only
- **Repositories** — all DB queries, return domain objects
- **Schemas** — all request validation and response serialisation
- **Models** — DB tables only, no business logic

Key conventions:
- Async/await throughout — no synchronous DB calls in async endpoints
- All endpoints declare explicit `response_model`
- Use `APIRouter` with prefix and tags — never define routes on the app directly
- Use `Pydantic Settings` for all config — no hardcoded values
- Use lifespan context manager in `main.py` — not deprecated `@app.on_event`

---

## 5. Hard Constraints (Non-Negotiables)

- **Authentication:** All endpoints authenticated by default via JWT. Unauthenticated endpoints must be explicitly approved.
- **Authorization:** Role-based access enforced at the service layer — never trust client-supplied roles.
- **Secrets:** No secrets, API keys, or credentials in source code — ever.
- **PII:** Never log passwords, tokens, ID numbers, or financial data.
- **Input Validation:** All inputs validated via Pydantic before reaching the service layer.
- **Dependencies:** Do not add packages without flagging first — ask before `uv add`.
- **Breaking Changes:** Do not modify existing API response schemas without versioning.
- **Migrations:** Never apply `--autogenerate` output without reviewing the generated script.
- **Spec Gate:** A spec without Gherkin is incomplete. A Gherkin scenario without a passing test is a lie.
- **Compliance behaviours** MUST have a Gherkin scenario — no exceptions.

---

## 6. Workflow Instructions

### Feature Kickoff Protocol
When given a new feature — even as a short description — follow this protocol automatically:

1. **Enter design mode** — do not write any code
2. **Activate relevant Skills** from the available skills (auth, testing, migrations, crud) based on the feature description — skills provide domain-specific rules and gotchas
3. **Produce two files:**
   - `specs/[feature].md` — data model, endpoints, architecture decisions, security/compliance notes
   - `tests/bdd/features/[feature].feature` — Gherkin in plain business language (no Python, no HTTP verbs)
4. **Wait for explicit approval** — do not create any other files
5. **On "proceed"** — implement, then run tests

Triggers automatically on: `"New feature: ..."`, `"Build: ..."`, `"Implement: ..."`, or any plain English business spec.

### Brainstorm Mode
When the user says **"change nothing"** or **"design only"** — propose, do not implement.

### Spec Types

| What | Format | Location |
|------|--------|----------|
| Business behaviour | Gherkin | `tests/bdd/features/` |
| Technical design | Markdown | `specs/` |
| Architecture decisions | ADR | `specs/adr/` |
| API contract | OpenAPI YAML | `specs/openapi.yaml` |

### Checkpointing
After each completed task, remind the user to commit and suggest a Conventional Commit message.

### Self-Updating Protocol
Suggest an AGENTS.md update when you:
- Correct a mistake that could recur → add to the relevant skill file
- Discover a missing convention
- Add a dependency with usage rules
- Identify an undocumented recurring pattern

Process: state the suggestion → wait for approval → update file AND changelog.

---

## 7. Code Review Checklist (Agent Self-Review)

Before declaring a task complete:

**Universal (always check):**
- [ ] No hardcoded secrets, credentials, or environment values
- [ ] All new endpoints have `response_model` declared
- [ ] All new endpoints are authenticated (or explicitly approved as public)
- [ ] Business logic is in the service layer — not in routers or models
- [ ] Database access is in the repository layer — not in services directly
- [ ] New dependencies added to `pyproject.toml` via `uv add`
- [ ] No existing tests deleted or skipped
- [ ] Ruff lint and mypy type checks pass
- [ ] AGENTS.md or relevant skill updated if a new convention was found

**Append skill-specific checklist items from any loaded Skills.**

---

## 8. Hard Constraints Reference
*(See Section 5 — listed here as checklist anchor)*
- [ ] Spec exists in `specs/` for this feature
- [ ] Gherkin scenario exists and is approved

---

## 9. VibeOps Principles

- **We validate everything** — "just trust the AI" is not an engineering practice
- **We measure actual impact** — "it feels faster" is not a metric
- **We adopt deliberately, not desperately** — every tool earns its place
- **We demand evidence-based practices** — not cargo-culted "best practices"
- **We move fast and build things that work** — not fast and break things
- In this brave new world, the ability to code a system matters less than the taste to know what it should become

---

## 10. Change Log

| Date       | Change                                                          | Author         |
|------------|-----------------------------------------------------------------|----------------|
| 2025-01-01 | Initial AGENTS.md created                                       | Natu Lauchande |
| 2025-01-15 | Added async SQLAlchemy 2.0 conventions                          | Natu Lauchande |
| 2025-02-01 | Added BDD/Gherkin rules and spec-first workflow                 | Natu Lauchande |
| 2025-02-20 | Added VibeOps principles section                                | Natu Lauchande |
| 2025-02-20 | Added self-updating protocol                                    | Natu Lauchande |
| 2025-02-21 | Renamed primary file from CLAUDE.md to AGENTS.md                | Natu Lauchande |
| 2025-02-21 | Added spec types table and dual-spec rule                       | Natu Lauchande |
| 2025-02-21 | Replaced feature kickoff prompt with auto protocol              | Natu Lauchande |
| 2026-02-21 | Added passlib/bcrypt incompatibility gotcha                     | Claude         |
| 2026-03-22 | Fixed repo URLs (natulauchande → vibeops-central org)           | Claw           |
| 2026-03-22 | v0.2.0 — 7 gotchas validated (Experiment 001)                   | Claw           |
| 2026-03-22 | v0.3.0 — Modularised into core + Skills (Experiment 002)        | Claw           |
