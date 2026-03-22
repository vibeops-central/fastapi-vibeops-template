# Experiment 001 — AGENTS.md v2 Gotchas Validation

**Date:** 2026-03-22
**Branch:** fix/agents-md-updates → merged as v0.2.0
**Status:** ✅ Validated

---

## Hypothesis

Adding specific rules (gotchas) to AGENTS.md produces measurably better agent output — specifically, fewer manual fixes needed to reach green tests.

---

## Method

1. Clone fresh template (v0.1.0 baseline)
2. Run: `New feature: user registration and JWT authentication`
3. Say `proceed`
4. Run tests cold — zero manual intervention
5. Record failures
6. Add rules to AGENTS.md
7. Repeat from step 1

---

## Results

| Round | AGENTS.md | Tests Passing | Manual Fixes |
|-------|-----------|--------------|--------------|
| 1 | v0.1.0 (original) | 2 / 19 | Yes |
| 2 | +3 gotchas | 0 / 19 (new errors) | Yes |
| 3 | +7 gotchas | **15 / 15** | **Zero** |

---

## Failures Discovered & Rules Added

| Failure | Rule Added |
|---------|-----------|
| `pydantic[email]` not installed | Always add `pydantic[email]` when using `EmailStr` |
| BDD step file missing | Every `.feature` must have a matching step file |
| SQLite pool config crash | Guard `pool_size`/`max_overflow` with sqlite check |
| `no such table` error | Call `create_all` in conftest for SQLite |
| `422` returned, `400` expected | Pydantic validation = 422; business rule = 400 |
| `401` returned, `403` expected | Unauthenticated = 401; forbidden = 403 |
| hatchling build failure | Prefer setuptools; hatchling needs `packages = ["src"]` |

---

## Outcome

Merged as PR #6 → tagged `v0.2.0`.

Coverage: 84%. Zero manual fixes on third run. Reproducibility confirmed on independent run.
