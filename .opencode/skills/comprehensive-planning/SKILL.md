---
name: comprehensive-planning
description: Use when the user asks to plan, design architecture, outline a project, or think through implementation strategy before writing code. Produces a touched-files list per phase for downstream use by subagents-swarm or direct execution.
---

# Comprehensive Planning Skill

When the user asks to plan, design, or think through an implementation strategy, follow this structured planning process. At each phase, maintain a **growing list of files to create/modify** so downstream execution (or the subagents-swarm skill) has a clear scope.

## Phase 1: Project Scan

Before proposing any plan, thoroughly understand the existing codebase:

1. **Scan directory structure** — understand the project layout, entry points, and conventions
2. **Read key config files** — `package.json`, `pyproject.toml`, `Cargo.toml`, `tsconfig.json`, `.env.example`, etc.
3. **Review existing patterns** — read 2-3 representative files to understand code style, naming, imports, testing conventions
4. **Identify related code** — grep for relevant symbols, functions, or modules
5. **Check for existing tests** — see what testing framework and patterns are in use
6. **Read AGENTS.md / README / CONTRIBUTING.md** — understand any project-specific instructions

**Files to change (initial candidates):** — list any files you've already identified as likely touch points based on this scan.

## Phase 2: Define Scope & Constraints

Surface the full picture before diving into solutions:

- **Goal**: What exactly needs to be built/changed? Write a one-sentence problem statement.
- **Success criteria**: How do we know it's done? (e.g., "all tests pass", "endpoint responds 200")
- **Constraints**: Time, budget, tech stack, performance, compatibility, security
- **Dependencies**: What does this depend on? What depends on this?
- **Risks**: What could go wrong? What's the hardest part?

**Files to change (refined):** — update the list: add files implied by the goal and constraints, remove false positives.

## Phase 3: Generate Options (Iterate)

For each meaningful approach, work through:

```
Option N: <short name>
├── Approach: How it works at a high level
├── Pros: What makes this good (specific, concrete)
├── Cons: What makes this bad (specific, concrete)
├── Effort: Rough estimate (small/medium/large + rationale)
├── Risk: Low / Medium / High (with reasoning)
└── Files to change: list of files specific to this option
```

- Generate **at least 2-3 options** (never stop at one)
- If the user already suggested an approach, include it as one option and add alternatives
- Be honest about tradeoffs — don't oversell your preferred option
- Ask the user for input: "Is there an approach I'm missing?"

**Files to change (per option):** — each option gets its own file list so the user can see the scope difference.

## Phase 4: Ask for Anything Related

Before finalizing, explicitly ask:

- "Are there any prior discussions, decisions, or docs I should read?"
- "Is there existing code that tried something similar?"
- "Are there constraints I haven't considered?"
- "Should I check with anyone else on the team?"

**Files to change (finalized):** — after user feedback, produce the definitive list of every file that will be created or modified, grouped by layer (models, services, API, tests, config).

## Phase 5: Deliver the Plan

Present the final plan with:

1. **Summary** — what we're building and why (1-2 sentences)
2. **Chosen approach** — which option and why
3. **Step-by-step implementation** — ordered checklist of concrete actions
   - Each step should be independently verifiable
   - Include test expectations per step
4. **Files to create/modify** — the finalized list from Phase 4, annotated with `(create)` or `(modify)`
5. **Open questions** — things to decide later
6. **Rollback plan** — how to undo if things go wrong

## Output for Downstream Skills

After the plan is accepted, produce a clean block of the touched files list that subagents-swarm or direct execution can consume:

```text
# Touched files (from comprehensive-planning)
CREATE:
  - src/services/payment.py
  - tests/unit/test_payment.py

MODIFY:
  - src/api/routes.py
  - src/models/order.py
```

## Verification

- After the plan is accepted, verify your understanding: "Before I start, let me confirm: <restate plan in your own words>"
- If the user says "just do it" without explicit plan review, still quickly scan the project first
