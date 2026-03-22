# Skills Modularisation — Design Doc

**Issue:** #7
**Branch:** feat/7-agents-core-skills-split
**Status:** Hypothesis — not validated

---

## Problem

`AGENTS.md` is growing into a monolith. Currently 350+ lines covering JWT gotchas, Alembic rules, BDD conventions, bcrypt incompatibilities, SQLite pool config, and more. An agent building a simple CRUD endpoint reads bcrypt rules that don't apply to it.

More importantly: the institutional knowledge encoded in AGENTS.md is trapped in each project. There's no way to share what you've learned.

---

## Hypothesis

Splitting AGENTS.md into a core conductor + domain-specific Skills modules will:
1. Keep agents focused — load only what's relevant to the task
2. Make Skills shareable across projects
3. Enable a community skills registry over time

---

## Proposed Design

### Core AGENTS.md (the conductor)
Owns everything that is universal and project-specific:
- Architecture rules (layered structure, async conventions)
- Hard constraints (no secrets, no passlib, no raw SQL)
- The Feature Kickoff Protocol
- Testing rules
- Self-updating protocol
- How to load Skills (see below)

Target size: < 150 lines.

### Skills (domain governance modules)
Live in `skills/` directory. Each is a self-contained markdown file:

```
skills/
  auth.md         — JWT, bcrypt, token patterns, known gotchas
  crud.md         — repository + service patterns for standard resources
  migrations.md   — Alembic rules, async setup, gotchas
  testing.md      — pytest-bdd async rules, SQLite setup, 422 vs 400
  background.md   — Celery, Redis, task queue conventions
```

### How Skills Get Loaded
The Feature Kickoff Protocol in core AGENTS.md instructs the agent to:
1. Read the feature description
2. Identify which Skills are relevant
3. Load those Skill files before proceeding

Example instruction in core AGENTS.md:
```
Before implementing any feature, identify and read relevant skills from skills/.
Auth-related work → skills/auth.md
Schema changes → skills/migrations.md
Test setup → skills/testing.md
```

---

## What Makes a Good Skill

A Skill is not documentation. It is **accumulated tribal knowledge**:
- Things that failed in production and the rule that prevents recurrence
- Gotchas discovered through experiments (like the pydantic[email] issue)
- Decisions made with reasons (why bcrypt directly, not passlib)

A Skill should answer: *"What do I wish I knew before I started?"*

---

## Experiment Design

To validate this hypothesis, we run the same benchmark used for AGENTS.md v2:

**Baseline (v0.2.0):** monolithic AGENTS.md, 15/15 tests, zero manual fixes.

**Experiment:**
1. Split AGENTS.md into core + skills/
2. Clone fresh template
3. Run: `New feature: user registration and JWT authentication`
4. Say `proceed`
5. Run tests cold — no manual fixes

**Success criteria:**
- 15/15 tests still passing
- Zero manual fixes
- Agent correctly self-loaded `skills/auth.md` and `skills/testing.md`
- Core AGENTS.md < 150 lines

**Failure criteria:**
- Test count drops
- Manual fixes required (means a gotcha got lost in the split)
- Agent ignored skill files

If it fails: figure out what got lost, fix the split, retry.

---

## Open Questions

1. Should Skills be versioned independently of AGENTS.md?
2. How does the agent know which Skills exist? Explicit list in core, or directory scan?
3. Can Skills depend on other Skills? (e.g. testing.md references patterns from auth.md)
4. Community skills registry — is `vibeops-central/skills` the right home, or per-project?

These are not blockers for the experiment. Validate the core split first.

---

## Not in Scope (yet)

- Community registry
- Skill versioning
- Cross-project skill sharing
- Public-facing copy updates

Those only happen if the experiment validates the concept.
