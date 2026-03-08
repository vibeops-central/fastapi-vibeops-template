---
name: vibeops-skill
description: >
  Universal VibeOps governance methodology for agentic coding environments. Load this skill
  whenever working in a VibeOps-governed repo (any repo with an AGENTS.md referencing VibeOps).
  Provides: Feature Kickoff Protocol, Spec-First Rule, Self-Updating Protocol, BDD/Gherkin rules,
  Code Review Checklist, and the 12 Vibing Factors. Stack-agnostic — works with any language or framework.
---

# VibeOps Skill — Universal Methodology Layer

This skill encodes what is **universally true** about governed agentic development.
Project-specific rules live in the project's `AGENTS.md`. This skill travels across all projects; `AGENTS.md` stays.

> Factor VIII — Skill Separation: "Methodology travels. Configuration stays."

---

## The 12 Vibing Factors

| # | Factor | Credo |
|---|--------|-------|
| I | Environment | "The agent is the instrument. The environment is the musician." |
| II | Spec First | "If it isn't written, it isn't agreed. If it isn't agreed, don't build it." |
| III | Living Contract | "Write it once as a promise. Run it forever as a test." |
| IV | Dual Spec | "One document for the business. One document for the machine. Neither alone is enough." |
| V | Sacred Tests | "A test that is changed to pass is a lie the codebase tells itself." |
| VI | Bug Taxonomy | "Every bug is a missing scenario. Fix the spec before you fix the code." |
| VII | Explicit Config | "If it lives only in someone's head, it will leave when they do." |
| VIII | Skill Separation | "Methodology travels. Configuration stays." |
| IX | Human Gate | "The agent proposes. The human decides. The environment learns." |
| X | Distance Metric | "Good code is not enough. It must also be yours." |
| XI | Experiment First | "Agent behaviour is not designed. It is discovered." |
| XII | Observable | "You cannot improve what you have not measured. You cannot trust what you have not observed." |

---

## Workflow Protocols

### Brainstorm Mode
When the user says **"change nothing"** or **"design only"**, enter planning mode:
- Review the codebase and propose a design
- Output a draft spec or Gherkin scenarios for review
- Do NOT touch any files until explicitly told to proceed

### Spec Types

| What | Format | Location |
|------|--------|----------|
| Business behaviour | Gherkin | `tests/bdd/features/` |
| Technical design | Markdown | `specs/` |
| Architecture decisions | ADR Markdown | `specs/adr/` |
| API contract | OpenAPI YAML | `specs/openapi.yaml` |
| Non-functional requirements | Markdown | `specs/` |

**Gherkin covers:** WHAT the system does from a user perspective — business rules, acceptance criteria, compliance behaviour.

**specs/ covers:** WHY and HOW decisions were made — data models, architectural choices, performance requirements, security threat model.

**Both must exist for any significant feature.**

---

### Feature Kickoff Protocol

When given a new feature name or business spec — even as a short description — automatically follow this protocol without being asked:

1. **Enter design mode immediately** — do not write any code
2. **Produce two files and nothing else:**
   - Technical design doc → `specs/[feature].md`
   - Gherkin scenarios → `tests/bdd/features/[feature].feature`
3. **`specs/[feature].md` must contain:**
   - Data model
   - API endpoints
   - Architectural decisions
   - Any security or compliance considerations
4. **Gherkin must be in plain business language:**
   - No Python, no HTTP verbs, no field names in Given/When/Then
   - Readable by a non-technical stakeholder
5. **Wait for explicit approval** before creating any other files
6. Only proceed to implementation when the user says **"proceed"**

This protocol triggers automatically on any message in the form:
- `"New feature: [description]"`
- `"Build: [description]"`
- `"Implement: [description]"`
- Any plain English business spec provided without a prior design

---

### Spec-First Rule

Before implementing any significant feature:
1. Check `/specs` for an existing technical design document
2. Check `tests/bdd/features/` for existing Gherkin scenarios
3. If neither exists, trigger the Feature Kickoff Protocol above
4. If a spec exists, **generate Gherkin scenarios from it** before writing any code
5. Both must be reviewed and approved before proceeding
6. Never write a route handler, schema, or service method without both approved

---

### Bug Fix Protocol

When a bug is reported:
1. **Identify the missing scenario** — every bug is a spec gap (Factor VI)
2. **Write the failing Gherkin scenario first** — before touching any code
3. **Get scenario approved** — confirm it captures the correct expected behaviour
4. **Then fix the code** to make the scenario pass
5. Never delete or rewrite an existing scenario to pass — fix the implementation

---

### Checkpointing

At the end of each completed task:
- Remind the user to commit the current state
- Suggest a meaningful commit message following **Conventional Commits** format
- Format: `type(scope): description`

---

### Self-Updating Protocol

Suggest an update to `AGENTS.md` when you:
- Correct a mistake that could recur → add to Tribal Knowledge
- Discover a missing convention that caused ambiguity
- Add a new dependency that has usage rules
- Identify a pattern used consistently that isn't documented

When suggesting an update:
1. State clearly: `"I suggest adding this to AGENTS.md — [section]: [rule]"`
2. Wait for explicit approval before modifying the file
3. After approval, update AGENTS.md AND add an entry to its Change Log

---

## BDD / Gherkin Rules (Universal)

- Feature files live in `tests/bdd/features/` — one file per resource
- Gherkin scenarios are generated from specs, **not from code**
- If a spec is ambiguous, surface the ambiguity as a question before writing the scenario
- Scenarios must be written in **business language** — no code, no HTTP verbs, no internal field names
- **Never rewrite a scenario to match broken behaviour** — fix the code, not the scenario
- Compliance-related behaviours MUST have a Gherkin scenario — they are the audit trail
- **Spec Gate:** A spec without Gherkin is incomplete. A Gherkin scenario without a passing test is a lie.

---

## Code Review Checklist (Agent Self-Review)

Before declaring any task complete:

**Specification**
- [ ] Technical spec exists in `specs/` for this feature
- [ ] Gherkin scenario exists and is approved

**Security**
- [ ] No hardcoded secrets, credentials, or environment values
- [ ] All new endpoints are authenticated (or explicitly approved as public)

**Architecture**
- [ ] Business logic is in the service layer, not in routers or models
- [ ] Data access is in the repository layer, not in services directly
- [ ] All new endpoints have `response_model` declared

**Dependencies & Schema**
- [ ] New dependencies added via `uv add`
- [ ] DB schema changes have a migration generated and reviewed

**Testing**
- [ ] Unit and integration tests added for all new code
- [ ] BDD feature file updated or created
- [ ] No existing tests deleted or skipped
- [ ] Lint and type checks pass

**Process**
- [ ] AGENTS.md updated if a new convention or correction was introduced
- [ ] Checkpoint suggested with a conventional commit message

---

## VibeOps Principles

- **We validate everything** — "just trust the AI" is not an engineering practice
- **We measure actual impact** — "it feels faster" is not a metric
- **We adopt deliberately, not desperately** — every tool earns its place
- **We demand evidence-based practices** — not cargo-culted "best practices"
- **We move fast and build things that work** — not fast and break things
- Configuration-driven development where AI tools operate within defined guardrails
- Test-first workflows where validation is automatic, not optional
- Sustainable AI adoption that improves code quality, not just velocity
- In this brave new world, the ability to code a system matters less than the taste to know what it should become
