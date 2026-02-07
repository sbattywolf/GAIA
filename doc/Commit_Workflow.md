# Simplified Commit Workflow

## Overview
This document outlines a streamlined workflow for committing and pushing changes to the GAIA repository. The goal is to reduce manual effort while maintaining a clean and organized commit history.

## Workflow Steps

### 1. Preparing Changes
- Ensure your branch is up-to-date with `develop`.
- Use `git pull origin develop` to fetch the latest changes.

### 2. Writing Commit Messages
- Follow the format: `<type>(<scope>): <description>`.
- **Types**:
  - `feat`: New feature.
  - `fix`: Bug fix.
  - `docs`: Documentation changes.
  - `chore`: Maintenance tasks.
- **Example**: `feat(auth): add token rotation support`.

### 3. Staging and Committing
- Stage changes: `git add <file>` or `git add .`.
- Commit changes: `git commit -m "<commit message>"`.

### 4. Pushing Changes
- Push to the remote branch: `git push origin <branch-name>`.
- Open a pull request (PR) on GitHub and assign reviewers.

## Automation
- Use pre-commit hooks to enforce code quality checks.
- Automate branch syncing with GitHub Actions.

## Best Practices
- Commit frequently with small, focused changes.
- Avoid committing directly to `main` or `develop`.
- Use draft PRs to share work in progress.

## Next Steps
- Finalize this document and add it to the repository.
- Set up pre-commit hooks for the repository.
- Train contributors on the simplified workflow.

---

*This document is a living artifact and should be updated as the project evolves.*