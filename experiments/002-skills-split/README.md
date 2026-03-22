# Experiment 002 — Skills Modularisation

**Date:** 2026-03-22  
**Status:** 🔄 In Progress  
**Branch:** `feat/7-agents-core-skills-split`  
**Issue:** [#7](https://github.com/vibeops-central/fastapi-vibeops-template/issues/7)

---

## Background

After Experiment 001, AGENTS.md is 350+ lines and covers everything from JWT gotchas to Alembic migrations in a single monolithic file. An agent building a simple CRUD endpoint must read bcrypt rules that don't apply to its task.

Two problems:
1. **Relevance noise** — agents process governance rules that don't apply to the current task
2. **Trapped knowledge** — the institutional knowledge in AGENTS.md is locked to one project with no mechanism to share it

The hypothesis is that splitting the monolith into a core conductor + domain-specific Skill files solves both.

---

## Hypothesis

Splitting AGENTS.md into a core file (<150 lines) and pluggable `skills/` modules will:
- Maintain the benchmark baseline (15/15 tests, zero manual fixes from Experiment 001)
- Keep governance knowledge modular and focused
- Create a foundation for cross-project skill sharing

---

## Proposed Structure

```
AGENTS.md           — core conductor: architecture rules, hard constraints,
                      Feature Kickoff Protocol, how to load Skills
skills/
  auth.md           — JWT, bcrypt, session patterns + gotchas from Exp 001
  testing.md        — pytest-bdd async rules, SQLite setup, 422 vs 400
  migrations.md     — Alembic rules, async setup, gotchas
  crud.md           — repository + service patterns
```

---

## Method

1. Split current AGENTS.md into core + skills/ on `feat/7-agents-core-skills-split`
2. Clone fresh template using the new branch
3. Run: `New feature: user registration and JWT authentication`
4. Say `proceed`
5. Run tests cold — zero manual intervention
6. Compare against Experiment 001 baseline

---

## Metrics to Capture

| Metric | How | Target |
|--------|-----|--------|
| Tests passing | `pytest` output | 15/15 (no regression) |
| Manual fixes | Human observation | Zero |
| Skill files loaded | Agent output / trace | auth.md + testing.md |
| Core AGENTS.md size | `wc -l AGENTS.md` | < 150 lines |
| Design phase time | `time claude -p "New feature..."` | < 90s |
| Implement phase time | `time claude --continue -p "proceed"` | < 8 min |
| Token usage | AWS Bedrock CloudWatch (if available) | TBD — baseline from Exp 001 |

## Success Criteria

- [ ] 15/15 tests passing (no regression)
- [ ] Zero manual fixes required
- [ ] Agent correctly self-loaded `skills/auth.md` and `skills/testing.md`
- [ ] Core AGENTS.md < 150 lines
- [ ] Total wall clock time comparable to Experiment 001 (~5 min)

## Failure Criteria

- Test count drops → a gotcha was lost in the split
- Manual fixes required → skill loading instruction too weak
- Agent ignored skill files → core needs stronger loading directive

---

## Results

*Pending experiment run.*

---

## Design Reference

See [`specs/skills-modularisation.md`](../../specs/skills-modularisation.md) for full design rationale and open questions.
