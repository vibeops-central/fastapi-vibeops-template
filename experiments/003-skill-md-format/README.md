# Experiment 003 — SKILL.md Standard Format (Progressive Disclosure)

**Date:** 2026-03-22
**Branch:** feat/7-agents-core-skills-split
**Status:** 🔄 Pending

---

## Background

Experiment 002 validated the Skills split (18/18, zero fixes) but introduced **+42s design overhead** vs the v0.2.0 baseline. Root cause: eager loading — the agent reads all 4 skill files upfront before writing the spec.

Victor Dibia's article (Feb 2026) and the Agent Skills open standard describe a better pattern: **progressive disclosure**. Skills have YAML frontmatter (name + description, ~100 tokens) injected at startup. Full content (~2,000 tokens) only loads when the task matches. With 4 skills: ~400 tokens at startup vs ~8,000 tokens with eager loading.

Additionally, adopting `SKILL.md` format makes our skills **natively compatible with Claude Code, Cursor, Gemini CLI, and 25+ other tools** — no custom tooling needed.

---

## Hypothesis

Converting skills from plain `.md` to `SKILL.md` format with YAML frontmatter will:
1. Reduce design phase overhead (target: back to ~60s from 102s)
2. Maintain 18/18 test pass rate and zero manual fixes
3. Make skills discoverable by Claude Code natively

---

## Changes from Experiment 002

- `skills/auth.md` → `skills/auth/SKILL.md` (+ YAML frontmatter)
- `skills/testing.md` → `skills/testing/SKILL.md` (+ YAML frontmatter)
- `skills/migrations.md` → `skills/migrations/SKILL.md` (+ YAML frontmatter)
- `skills/crud.md` → `skills/crud/SKILL.md` (+ YAML frontmatter)

Each SKILL.md has:
```yaml
---
name: auth
description: <one-line description for progressive disclosure>
allowed-tools: Read, Write, Edit, Bash
---
```

---

## Method

1. Clone branch `feat/7-agents-core-skills-split` (contains SKILL.md format)
2. Time design phase: `New feature: user registration and JWT authentication`
3. Time implement phase: `proceed`
4. Run tests cold — zero manual intervention
5. Compare against Exp 002 baseline

---

## Metrics to Capture

| Metric | Exp 002 Baseline | Target |
|--------|-----------------|--------|
| Tests passing | 18 / 18 | ≥ 18 / 18 |
| Manual fixes | 0 | 0 |
| Coverage | 83% | ≥ 80% |
| Design time | 102s | ~60s |
| VibeOps Score | 96.6 | ≥ 96.6 |

---

## Results

*Pending experiment run.*
