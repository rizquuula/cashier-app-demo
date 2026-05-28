---
name: autonomous-work
description: Use when the user is AFK (away from keyboard) and wants the session to work independently. AI makes implementation decisions autonomously, handles errors, and reports results.
---

# Autonomous Work Skill

When the user says they're AFK or explicitly asks for autonomous execution, follow these rules to make sound decisions independently while minimizing risk.

## Mindset

- The user is **not watching** — every decision must be safe by default
- When in doubt, **do the reversible thing** — prefer changes that are easy to undo
- If you can't proceed, **stop and summarize** rather than making risky guesses
- **No unnecessary questions** — the user is AFK and won't answer. Default to your best judgment.

## Decision-Making Heuristics

When you hit a choice point, resolve it autonomously:

| Scenario | Default Action |
|---|---|
| Naming convention | Follow existing patterns in the codebase (grep for similar symbols) |
| Library choice | Use what the project already has (check package.json, imports, etc.) |
| API design | Match existing endpoints in the project |
| Error handling | Be defensive — log, wrap in try/except, return safe defaults |
| Configuration | Use sensible defaults + env var overrides |
| Test coverage | Add tests for every new function |
| Test framework | Use whatever the project already uses |
| Minor UI decisions | Match existing components/styles |

If the decision is **truly arbitrary** (no existing pattern, no clear winner), pick the simplest option and note it in the final report.

## Execution Flow

### 1. Plan Briefly (internal)

Before touching anything, quickly:
- List the steps in order
- Identify the files to change
- Note any risky operations (deletions, renames, schema changes)

### 2. Execute Step by Step

- One step at a time, verify each before moving on
- After each step, run the relevant tests / lint / type-check
- If a step fails, retry once with debug output; if it fails again, skip it and note the issue

### 3. Handle Errors Autonomously

| Error | Response |
|---|---|
| Test fails | Fix the code, not the test (unless test is wrong) |
| Lint/type error | Auto-fix if possible (`ruff --fix`, etc.) |
| Import missing | Install the package (if in project manifest) or polyfill |
| Ambiguous spec | Pick the most common pattern in the codebase |
| API/dependency down | Retry once with backoff, then stub and note |
| Permission denied (tool) | Skip the operation, note it in the report |

**Never** delete files or data without being 100% certain — if unsure, leave a TODO and move on.

### 4. Checkpoint Frequently

- After every meaningful chunk, do a quick sanity check:
  - Do the tests still pass?
  - Does the app still start/compile?
  - Are there any new lint errors?
- If the project uses git, commit after each logical milestone (the user can squash later)

### 5. Final Report

When work is complete (or blocked), produce a summary:

```
## Autonomous Work Report

### Status: ✅ Complete / ⚠️ Partial / ❌ Blocked

### Changes Made
- file1.py — added X function
- file2.py — refactored Y
- tests/test_x.py — new tests

### Test Results
- unit: 12 passed, 0 failed
- lint: clean
- type-check: clean

### Decisions Made
- Used asyncio over threading (project convention)
- Chose pydantic v2 models (matching existing code)

### Issues Encountered
- Third-party API rate-limited; added retry with backoff
- Skipped migration test (needs local DB — add later)

### Next Steps (if any)
- Remaining work: [list]
- Things the user should review: [list]
```

## What NOT to Do

- ❌ Do not ask questions — make the best call and note it
- ❌ Do not delete or overwrite files without clear evidence it's safe
- ❌ Do not push to production branches or deploy
- ❌ Do not install random packages without checking if they're already in the project
- ❌ Do not run destructive commands (`rm -rf`, `DROP TABLE`, etc.) unless explicitly asked
- ❌ Do not change formatting/whitespace across the entire project (stay in scope)
- ✅ Do stop and produce a report if you're stuck, blocked, or confused
