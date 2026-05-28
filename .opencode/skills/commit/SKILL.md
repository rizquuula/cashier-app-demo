---
name: commit
description: Use when the user asks to commit, stage, or write a commit message. Provides conventional commit prefixes and ensures no co-author trailers are added.
---

# Commit Skill

When the user asks you to commit changes or write a commit message, follow these rules:

## Commit Message Format

Use the **Conventional Commits** format:

```
<type>: <short description>

<body (optional)>
```

Allowed types:
- `feat:` — A new feature
- `fix:` — A bug fix
- `chore:` — Maintenance, tooling, dependencies, CI config
- `bump:` — Version bumps, dependency updates
- `docs:` — Documentation only changes
- `refactor:` — Code change that neither fixes a bug nor adds a feature
- `style:` — Formatting, missing semicolons, etc. (no code change)
- `test:` — Adding or updating tests
- `perf:` — A code change that improves performance
- `ci:` — CI configuration and scripts
- `build:` — Changes that affect the build system
- `revert:` — Reverts a previous commit

## Rules

1. Always prefix the commit message with the appropriate type from above.
2. Keep the first line under 72 characters.
3. Use the imperative mood ("add feature" not "added feature" or "adds feature").
4. Do NOT add any `Co-authored-by:` trailers.
5. Do NOT add any other trailers (like `Signed-off-by:`, `Reviewed-by:`, etc.).
6. The body (if present) is separated from the summary by a blank line.

## Examples

```
feat: add user login endpoint
fix: prevent null pointer in order total calculation
chore: update eslint config to v9
bump: upgrade axios from 1.6.0 to 1.7.0
docs: update API readme with new endpoints
refactor: extract payment validation logic
```

## Workflow

When the user says "commit" or "commit changes":
1. Run `git diff` and `git status` to see what's staged and unstaged.
2. Based on the changes, determine the appropriate commit type.
3. Write a concise commit message following the rules above.
4. Run `git commit -m "<message>"` (no co-author or trailers).
