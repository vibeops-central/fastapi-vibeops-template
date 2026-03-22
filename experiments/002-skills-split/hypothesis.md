# Experiment 002 — Skills Modularisation

**Date:** 2026-03-22
**Branch:** feat/7-agents-core-skills-split
**Status:** 🔄 In Progress

---

## Hypothesis

Splitting AGENTS.md into a core conductor + domain-specific Skills modules will maintain or improve benchmark scores while making governance knowledge shareable across projects.

---

## Method

1. Split AGENTS.md into `AGENTS.md` (core, <150 lines) + `skills/` directory
2. Clone fresh template
3. Run: `New feature: user registration and JWT authentication`
4. Say `proceed`
5. Run tests cold — zero manual intervention
6. Compare results against v0.2.0 baseline (15/15, zero manual fixes)

---

## Success Criteria

- [ ] 15/15 tests passing (no regression from v0.2.0)
- [ ] Zero manual fixes
- [ ] Agent correctly loaded relevant skill files
- [ ] Core AGENTS.md < 150 lines

## Failure Criteria

- Test count drops → means a gotcha was lost in the split
- Manual fixes required → means the skill loading mechanism doesn't work
- Agent ignored skill files → means the instruction in core needs to be stronger

---

## Results

*Pending experiment run.*
