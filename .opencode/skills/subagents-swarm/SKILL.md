---
name: subagents-swarm
description: Use when implementing a multi-file change that can be parallelized across independent files. Spawns subagents to work on separate file groups, keeping the main session lean.
---

# Subagents Swarm Skill

When a task touches multiple files, use subagents to parallelize work and keep the main session uncluttered.

## Step 1: Identify Touched Files

Determine which files need to be created or modified:

- **If a planning phase produced a touched-files list**, use it directly
- **If not**, scan the codebase to discover what needs changing: look at import graphs, grep for relevant symbols, read key modules
- Group files by dependency: files that depend on each other go in the same group; files with no cross-dependencies can be separate groups
- Output the file list explicitly so subagents have clear scope

## Step 2: Partition Into Independent Groups

Split the touched files into **independent batches**:

```
Batch A: models/product.py, models/cart.py          (model layer)
Batch B: services/inventory.py, services/pricing.py  (service layer)
Batch C: api/routes.py, api/schemas.py               (API layer)
```

Rules:
- Files in the same batch must have no circular dependencies
- Each batch should have 1-3 files (small batches are easier to verify)
- Shared utility files (types, constants, base classes) should go in the batch they're first needed, or a shared "foundation" batch
- If a batch depends on another (e.g., API depends on models), order them sequentially

## Step 3: Spawn Subagents with Task Tool

For each independent batch, spawn a **subagent** using the `task` tool:

```
Task agent type: general
Prompt structure per subagent:
  - Context: what the overall task is (for coherence)
  - Scope: EXACTLY which files this subagent owns
  - Instructions: what to do (implement, refactor, fix, test)
  - Constraints: coding conventions to follow (from AGENTS.md or project patterns)
  - Verification: how to verify the work (lint, type-check, test commands)
  - Output: what to report back (changes made, files created, issues found)
```

Example prompt for a subagent:

```
The overall project is adding a checkout flow. Your scope is limited to:
  - src/services/payment.py (create)
  - src/services/inventory.py (modify)

Tasks:
  1. Create payment.py with process_payment(order_id, amount) function
  2. Add reserve_items(cart_items) to inventory.py

Conventions:
  - Use pydantic models, async/await pattern
  - Existing style: dataclasses, type annotations, function-level docstrings

Verify:
  - python -m pytest tests/unit/test_payment.py -v
  - ruff check src/services/
```

## Step 4: Collect Results

When each subagent completes, collect:
- What was created/modified
- Any issues or design decisions made
- Verification results (tests passing, lint clean)

If a subagent failed or hit a blocker:
- Assess whether the batch is truly blocked or can proceed with stubs
- Resolve blockers in the main session or re-spawn with more context

## Step 5: Integration Pass

After all subagents report success, run a final integration check:

1. Run the full test suite
2. Run lint + type-check on all changed files
3. Verify cross-batch interactions work (e.g., API actually calls the new service)
4. If something is broken, fix it in the main session (small fix) or re-spawn a subagent (large fix)

## Why This Works

- **Main session stays clean** — bulk implementation work is delegated; only structure and integration remain
- **Parallelism** — independent batches run concurrently
- **Focused subagents** — each agent only sees the files it owns, reducing confusion
- **Verifiable chunks** — each batch is independently testable

## When NOT to Swarm

- The change touches only 1-2 files → just do it in the main session
- Files are so tightly coupled they can't be partitioned → do it sequentially
- The task is pure research or exploration → no files to touch
- The user explicitly asked for a single, cohesive implementation → honor their preference
