# fastapi-vibeops-template

A reference implementation of a VibeOps-primed FastAPI environment.

Part of the [VibeOps framework](https://github.com/natulauchande/vibeops) — a systematic approach to AI-assisted development that moves beyond vibe coding to structured, measurable, self-improving engineering environments.

---
## Results of experiment with this branch vs Yolo branch ( no Agents branch)

# VibeOps Configuration Effectiveness — Experiment Results

> **Research Question:** Does a VibeOps-primed environment (AGENTS.md) produce measurably better AI-generated code than an unprimed environment?

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Model** | Claude Sonnet 4 (via Claude Code) |
| **Template Repo** | `nlauchande/fastapi-vibeops-template` |
| **Task** | User Management API (CRUD + auth + validation) |
| **Condition A** | No AGENTS.md — raw Claude Code |
| **Condition B** | AGENTS.md + CLAUDE.md symlink present |

Same model. Same template. Same prompt. Different environment.

---

## Composite Vibecheck Score

| Condition | Vibecheck Score | Rating |
|-----------|:--------------:|--------|
| **A — Control (No VibeOps)** | **0.510** | ⚠️ |
| **B — VibeOps (AGENTS.md)** | **0.932** | ✓ |
| **Δ (B − A)** | **+0.422 (+82.8%)** | |

---

## Dimension Breakdown

| Dimension | Weight | Condition A | Condition B | Δ (Raw) | Δ (Weighted) |
|-----------|:------:|:-----------:|:-----------:|:-------:|:------------:|
| Architecture | 30% | 0.70 | 0.95 | +0.25 | +0.075 |
| Security | 20% | 0.30 | 0.95 | **+0.65** | **+0.130** |
| Testing | 20% | 0.60 | 0.90 | +0.30 | +0.060 |
| Code Quality | 15% | 0.80 | 0.90 | +0.10 | +0.015 |
| Spec Adherence | 15% | 0.00 | 0.95 | **+0.95** | **+0.142** |
| **Composite** | **100%** | **0.510** | **0.932** | **+0.422** | **+0.422** |

---

## Structural Output Comparison

| Metric | Condition A | Condition B | Δ |
|--------|:----------:|:----------:|:-:|
| Python files | 17 | 35 | +18 |
| Test files | 2 | 5 | +3 |
| Test lines | 146 | 656 | +510 |
| Source lines | 241 | 366 | +125 |
| Test:Source ratio | 0.61 | 1.79 | +1.18 |
| Test layers | 1 | 3 | +2 |
| Gherkin scenarios | 0 | 11 | +11 |

---

## Feature Presence

| Capability | Condition A | Condition B |
|-----------|:----------:|:----------:|
| Service layer | ✗ | ✓ |
| Repository layer (class-based) | ✗ | ✓ |
| API versioning (`/api/v1/`) | ✗ | ✓ |
| Authentication (bcrypt + JWT) | ✗ | ✓ |
| Alembic migrations | ✗ | ✓ |
| Makefile | ✗ | ✓ |
| Specs directory | ✗ | ✓ |
| BDD / Gherkin scenarios | ✗ | ✓ |
| Unit tests | ✗ | ✓ |
| Integration tests | ✓ | ✓ |
| Anti-enumeration test | ✗ | ✓ |
| `uv.lock` checked in | ✗ | ✓ |

---

## Key Findings

1. **Security is the largest raw delta (+0.65).** Without AGENTS.md, the agent produced zero authentication. With AGENTS.md, it implemented bcrypt + JWT, password validation, email normalisation, and anti-enumeration responses — because Section 5 (Hard Constraints) mandates auth-by-default.

2. **Spec adherence is the largest absolute gap (0.00 → 0.95).** The Feature Kickoff Protocol in AGENTS.md forced the agent to produce `specs/auth.md` and `tests/bdd/features/auth.feature` before writing any code. Without it, the agent skipped straight to implementation.

3. **Code quality is the smallest delta (+0.10).** The model writes decent code either way — clean Pydantic v2, proper pagination, good naming. VibeOps doesn't make the code prettier; it makes the *system* more complete.

4. **The constrained branch was faster to generate.** Counterintuitive: more rules = less decision paralysis = fewer wrong turns = faster completion. Constraints are faster than choices.

5. **Tribal knowledge transferred.** The agent used `bcrypt` directly instead of `passlib` (Section 9 gotcha), used `sync_client` for BDD steps (Section 9 gotcha), and used `select()` over `session.query()` (Section 4). These are mistakes it would have had to discover and fix without AGENTS.md.

---

## Prompt Used (Both Conditions)

```
Build a user management API with the following requirements:
- User model with fields: id, email, full_name, is_active, created_at
- CRUD endpoints: create user, get user by id, list users with pagination, update user, delete user
- Input validation on email format and required fields
- Proper error responses for not found and duplicate email
```



## What This Is

This is not a minimal starter template. It is a **reference implementation** — a fully primed example of what a mature VibeOps environment looks like in practice.

The `AGENTS.md` file at the root is intentionally comprehensive. It is the primary artefact of this repo. Everything else — the FastAPI skeleton, the BDD structure, the spec conventions — exists to demonstrate that the rules in `AGENTS.md` produce real, working output.

---

## What VibeOps Is

VibeOps is the discipline layer on top of AI-assisted development.

Same prompt. Two outcomes:

| Without VibeOps | With VibeOps |
|-----------------|--------------|
| Agent guesses the package manager | Agent reads `AGENTS.md`, uses `uv` |
| Hardcoded secrets, weak hashing | Pydantic Settings, bcrypt, env-driven config |
| Tests deleted to pass CI | Tests protected, code fixed instead |
| Logic dumped into routers | Layered architecture enforced |

The `AGENTS.md` is what makes the difference. It is the agent's onboarding document, constraint system, and tribal knowledge base — all in one file.

> *In this brave new world, the ability to code a system matters less than the taste to know what it should become.*

---

## How to Use This Template

### Option 1 — Learn from it

Read `AGENTS.md` end to end. Understand what each section does and why it exists. Then build your own for your stack.

The sections that matter most:
- **Section 5** — Hard Constraints: what your team's non-negotiables are
- **Section 6** — Workflow Instructions: how your team starts features and fixes bugs
- **Section 9** — Tribal Knowledge: the real gotchas from real sessions

### Option 2 — Fork and adapt it

```bash
git clone https://github.com/natulauchande/fastapi-vibeops-template
cd fastapi-vibeops-template
ln -s AGENTS.md CLAUDE.md    # Claude Code compatibility
cp .env.example .env
uv sync
```

Then strip what doesn't apply to your team and add what does. The `AGENTS.md` should reflect your stack, your constraints, and your tribal knowledge — not ours.

### Option 3 — Drop it into an existing repo

Copy `AGENTS.md` into your repo root. Update:
1. Section 1 — your stack and purpose
2. Section 2 — your actual build commands
3. Section 3 — your actual repo structure
4. Section 5 — your actual hard constraints
5. Section 9 — your actual tribal knowledge

Everything else can stay as-is until your team finds something to correct.

---

## The AGENTS.md Is the Product

Most templates ship code. This template ships an **environment**.

The `AGENTS.md` encodes:

```
Expert knowledge     → so juniors produce senior-level output
Hard constraints     → so the agent never violates your standards
Tribal knowledge     → so past mistakes don't repeat
Workflow protocols   → so every session starts the same disciplined way
Self-updating rules  → so the file improves itself from real sessions
```

The Vibecheck Score measures how well the environment is working. The higher the score, the smaller the gap between your best engineer and your newest one.

---

## The Self-Updating Protocol

`AGENTS.md` is designed to improve itself. When the agent discovers something worth capturing — a gotcha, a missing rule, a pattern — it proposes an update:

```
"I suggest adding this to AGENTS.md — Section 9: [rule]"
```

You approve. The file is updated. The change is logged.

Every session makes the environment stronger. This is not a file you maintain — it is a file that learns.

---

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Runtime | Python 3.11 | Stable, widely supported |
| Framework | FastAPI | Async-first, Pydantic-native |
| Package manager | uv | Fast, modern, reproducible |
| ORM | SQLAlchemy 2.0 async | Type-safe, async-native |
| Migrations | Alembic | Standard, reliable |
| Testing | pytest + pytest-asyncio | Async-native test suite |
| BDD | pytest-bdd | Gherkin as living spec |
| Linting | ruff | Fast, comprehensive |
| Type checking | mypy | Catches what ruff misses |

---

## Project Structure

```
src/           FastAPI application (layered architecture)
tests/         Unit, integration, and BDD tests
tests/bdd/features/  Gherkin feature files — one per resource
specs/         Technical design docs and ADRs
experiments/   MLflow experiment configs (Vibecheck Score tracking)
vibecheck/     Vibecheck Score computation library (coming Phase 3)
AGENTS.md      The environment — primary artefact of this repo
CLAUDE.md      Symlink → AGENTS.md (Claude Code compatibility)
```

---

## Vibecheck Score

The Vibecheck Score measures how well your environment is working — a leading indicator of output quality before a line of code is written.

```bash
uv run vibecheck .

# ─────────────────────────────
# Vibecheck Score: 0.91
# ├── Security:       1.00  ✓
# ├── Architecture:   0.88  ✓
# ├── Testing:        0.91  ✓
# ├── Compliance:     0.85  ~
# └── Process:        0.94  ✓
# ─────────────────────────────
```

Coming in Phase 3. Tracked via MLflow in Phase 4.

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 0 | ✅ Done | AGENTS.md + repo structure |
| 1 | 🔄 In progress | Working FastAPI skeleton with auth |
| 2 | ⏳ Planned | Full todo app — spec → Gherkin → implementation |
| 3 | ⏳ Planned | Vibecheck Score CLI |
| 4 | ⏳ Planned | MLflow experiment integration |
| 5 | 🔭 Future | Self-optimising AGENTS.md via DSPy |

---

## Learn More

- [VibeOps Manifesto](https://github.com/natulauchande/vibeops)
- [Machine Learning Engineering with MLflow](https://www.packtpub.com/product/machine-learning-engineering-with-mlflow/9781800562882) — Natu Lauchande
- PyCon Africa 2025 — where VibeOps concepts were first presented
- EuroPython 2026 — full VibeOps framework talk (coming)

---

## License

MIT — use it, fork it, adapt it, share it freely.

Built by [Natu Lauchande](https://github.com/natulauchande) · #VibeOps
