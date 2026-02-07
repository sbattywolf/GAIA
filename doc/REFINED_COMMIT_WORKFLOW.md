# Refined Commit Workflow for GAIA Repository

## Purpose
This document outlines a refined commit workflow to ensure consistency, traceability, and alignment with GAIA's hybrid goals and service-oriented architecture.

## Commit Message Format

### Conventional Commits
Adopt the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Commit Types
- **feat**: A new feature.
- **fix**: A bug fix.
- **docs**: Documentation changes.
- **style**: Code style changes (e.g., formatting).
- **refactor**: Code refactoring without functional changes.
- **perf**: Performance improvements.
- **test**: Adding or updating tests.
- **chore**: Maintenance tasks (e.g., dependency updates).

### Scope
- Use a short, lowercase noun describing the area of the codebase (e.g., `auth`, `ci`, `docker`).

### Description
- Write a concise summary of the change.
- Use the imperative mood (e.g., "add token rotation").

### Examples
- `feat(auth): add token rotation`
- `fix(ui): resolve button overlap issue`
- `docs(readme): update hybrid configuration section`

## Workflow

### 1. **Before Committing**
- Ensure your branch is up-to-date with `develop`.
- Run tests locally to verify changes.
- Format code using the project's linter.

### 2. **Writing Commit Messages**
- Follow the Conventional Commits format.
- Use meaningful and descriptive messages.

### 3. **Committing Changes**
- Stage changes selectively using `git add -p`.
- Use `git commit` with the appropriate message format.

### 4. **Pushing Changes**
- Push to the remote branch using `git push`.
- Open a pull request (PR) for review.

## Hybrid Configuration Considerations

### AI/LLM Integration
- Use `feat(ai)` for AI/LLM-related changes.
- Include detailed descriptions for AI/LLM features.

### Service-Oriented Architecture
- Use `feat(service)` for modular service changes.
- Include service-specific details in the commit body.

### Workflow Automation
- Use `chore(workflow)` for CI/CD updates.
- Document automation changes in the commit body.

## Best Practices
- Write atomic commits: one logical change per commit.
- Use draft PRs to share work in progress.
- Rebase interactively to clean up commit history.
- Avoid committing sensitive information.

---

This refined workflow ensures GAIA's commit practices are consistent, scalable, and aligned with its hybrid goals.