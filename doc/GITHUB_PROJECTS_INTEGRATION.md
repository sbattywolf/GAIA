# GitHub Projects Integration Guide

## Overview

GAIA has **built-in support** for GitHub Projects V2 integration. When configured, issues labeled with `sprint/*` are automatically added to your GitHub Project board.

## Current Integration Status

✅ **IMPLEMENTED** - GitHub Projects integration is available but requires configuration.

### What's Already Implemented

1. **Automated Issue Addition** (`.github/workflows/sprint_onboard.yml`)
   - Automatically adds issues to GitHub Projects when labeled with `sprint/*`
   - Works with both user and organization Projects
   - Adds a checklist to sprint issues automatically

2. **Database Sync Agent** (`agents/github_sessions_sync.py`)
   - Syncs `gaia.db` backlog → GitHub Issues
   - Supports dry-run mode for testing
   - Tags issues with `GAIA_ID` for tracking

3. **Documentation** (`doc/AGENT_SESSION_WORKFLOW.md`)
   - Architecture and design principles
   - One-way sync from gaia.db → GitHub
   - Approval and gating requirements

## How to Enable GitHub Projects Integration

### Step 1: Create a GitHub Project

1. Go to https://github.com/users/sbattywolf/projects (for personal projects)
   - Or https://github.com/orgs/YOUR_ORG/projects (for organization projects)

2. Click **"New project"**

3. Choose a template (e.g., "Team backlog") or start from scratch

4. Note your **Project Number** (visible in the URL: `https://github.com/users/sbattywolf/projects/NUMBER`)

### Step 2: Configure Repository Secrets

Add the `PROJECT_V2_NUMBER` secret to your repository:

1. Go to repository **Settings** → **Secrets and variables** → **Actions**

2. Click **"New repository secret"**

3. Name: `PROJECT_V2_NUMBER`
   Value: Your project number (e.g., `1`, `2`, etc.)

4. Click **"Add secret"**

### Step 3: Test the Integration

1. Create a test issue in your repository

2. Add a label starting with `sprint/` (e.g., `sprint/current`, `sprint/2026-02`)

3. The workflow will automatically:
   - Add a checklist to the issue
   - Add the issue to your GitHub Project (if `PROJECT_V2_NUMBER` is configured)

4. Check your GitHub Project board to verify the issue appears

## Using the Database Sync Agent

The `github_sessions_sync.py` agent syncs your local backlog database to GitHub Issues.

### Dry-Run Mode (Safe Testing)

```bash
# Preview what would be synced (no changes made)
python agents/github_sessions_sync.py --dry-run
```

### Live Sync Mode

**Prerequisites:**
- `gaia.db` must exist (run `python agents/sync_backlog_to_db.py` first)
- Set environment variables:
  - `AUTOMATION_GITHUB_TOKEN` - GitHub Personal Access Token with `repo` scope
  - `AUTOMATION_GITHUB_REPOSITORY` - Repository in format `owner/repo`

```bash
# Sync backlog to GitHub Issues
export AUTOMATION_GITHUB_TOKEN="ghp_your_token_here"
export AUTOMATION_GITHUB_REPOSITORY="sbattywolf/GAIA"
python agents/github_sessions_sync.py
```

**What it does:**
- Creates GitHub issues for items in `gaia.db` backlog table
- Tags issues with `GAIA_ID: <id>` in the body for tracking
- Updates existing issues if they already exist
- Sets labels based on priority (e.g., `gaia:high`)

### Token Preferences

The sync agent checks for tokens in this order:
1. `AUTOMATION_GITHUB_TOKEN_PAI` (personal automation token)
2. `AUTOMATION_GITHUB_TOKEN` (general automation token)
3. `AUTOMATION_GITHUB_TOKEN_ORG` (organization automation token)
4. `GITHUB_TOKEN` (fallback)

Repository checks:
1. `AUTOMATION_GITHUB_REPOSITORY`
2. `AUTOMATION_GITHUB_REPO`
3. `GITHUB_REPO`
4. `GITHUB_REPOSITORY` (fallback)

## Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                Local Data Sources                        │
├─────────────────────────────────────────────────────────┤
│  doc/todo-archive.ndjson    → Task tracking             │
│  gaia.db                    → SQLite database           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│            github_sessions_sync.py Agent                 │
├─────────────────────────────────────────────────────────┤
│  • Reads from gaia.db                                   │
│  • Creates/updates GitHub Issues                        │
│  • Adds GAIA_ID tags for tracking                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                 GitHub Issues                            │
├─────────────────────────────────────────────────────────┤
│  • Backlog items as issues                              │
│  • Tagged with GAIA_ID                                  │
│  • Labeled by priority                                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│          GitHub Projects (when labeled)                  │
├─────────────────────────────────────────────────────────┤
│  • Issues with sprint/* labels                          │
│  • Automatically added via workflow                     │
│  • Visible on project board                             │
└─────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Single Source of Truth**: `gaia.db` is authoritative for runtime state
2. **One-Way Sync**: Data flows from gaia.db → GitHub (read-only view)
3. **Opt-In**: Remote sync requires explicit configuration
4. **Audit Trail**: All sync operations are logged
5. **Approval Gated**: Remote writes require CHECKPOINT approval

## Security & Token Management

### Token Scopes Required

For GitHub Projects integration, your Personal Access Token needs:
- `repo` (full control of private repositories)
- `project` (full control of projects)

### Creating a Token

1. Go to GitHub **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Set expiration (recommend 90 days with rotation)
4. Select scopes: `repo` and `project`
5. Generate and copy the token
6. Store securely (see [SECRETS_MANAGEMENT_GUIDE.md](SECRETS_MANAGEMENT_GUIDE.md))

### Token Storage

**Recommended** (using GAIA secrets manager):
```bash
python scripts/secrets_cli.py set AUTOMATION_GITHUB_TOKEN your_token_here
```

**Alternative** (using .env):
```bash
echo "AUTOMATION_GITHUB_TOKEN=your_token_here" >> .env
```

## Workflows Using GitHub Projects

### Workflow 1: Sprint Planning

1. Create tasks in `doc/todo-archive.ndjson` or `gaia.db`
2. Sync to GitHub Issues: `python agents/github_sessions_sync.py`
3. Label issues with `sprint/current` or `sprint/2026-02`
4. Workflow automatically adds them to your Project board
5. Manage sprint in GitHub Projects UI

### Workflow 2: Issue Triage

1. Create issues manually in GitHub
2. Add `sprint/*` label to include in current sprint
3. Workflow adds checklist and adds to Project
4. Update issue status in GitHub Projects

### Workflow 3: Backlog Management

1. Maintain backlog in `gaia.db`
2. Periodically sync: `python agents/github_sessions_sync.py`
3. Issues appear in GitHub
4. Label sprint items to add to Project board
5. Track progress in both local dashboard and GitHub Projects

## Troubleshooting

### Project Not Adding Issues

**Problem**: Issues with `sprint/*` labels aren't appearing in Project

**Solutions**:
1. Verify `PROJECT_V2_NUMBER` secret is set correctly
2. Check workflow logs in Actions tab
3. Ensure token has `project` scope
4. Verify project number in URL

### Sync Failing

**Problem**: `github_sessions_sync.py` fails or times out

**Solutions**:
1. Run in dry-run mode first: `--dry-run`
2. Verify `gaia.db` exists
3. Check token is valid: `gh auth status`
4. Verify environment variables are set
5. Check API rate limits: `gh api rate_limit`

### Duplicate Issues

**Problem**: Multiple issues created for same backlog item

**Solutions**:
1. Agent searches by `GAIA_ID` tag to prevent duplicates
2. Manually delete duplicate issues
3. Re-run sync - it will find existing issues

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AUTOMATION_GITHUB_TOKEN` | Yes (for sync) | - | GitHub token with repo scope |
| `AUTOMATION_GITHUB_REPOSITORY` | Yes (for sync) | - | Repository in owner/repo format |
| `PROJECT_V2_NUMBER` | Yes (for auto-add) | - | GitHub Project number |
| `PROTOTYPE_USE_LOCAL_EVENTS` | No | `0` | Set to `1` for local-only mode |

### Repository Secrets

Add these in **Settings** → **Secrets and variables** → **Actions**:

| Secret | Required | Description |
|--------|----------|-------------|
| `PROJECT_V2_NUMBER` | For auto-add | GitHub Projects V2 project number |
| `AUTOMATION_GITHUB_TOKEN` | For workflows | GitHub token for automation |

## Related Documentation

- [AGENT_SESSION_WORKFLOW.md](AGENT_SESSION_WORKFLOW.md) - Architecture and design
- [SECRETS_MANAGEMENT_GUIDE.md](SECRETS_MANAGEMENT_GUIDE.md) - Token storage
- [GITHUB_2FA_GUIDE.md](GITHUB_2FA_GUIDE.md) - Token management with 2FA
- [AGENT_AUTOMATION_TOKENS.md](AGENT_AUTOMATION_TOKENS.md) - Token scopes and rotation

## Future Enhancements

Planned improvements:

- [ ] Two-way sync (GitHub → gaia.db)
- [ ] Support for Project custom fields
- [ ] Automatic status updates based on issue state
- [ ] Batch sync with rate limiting
- [ ] Web UI for sync management
- [ ] GitHub App integration (no PAT required)

## FAQ

### Q: Is GitHub Projects required to use GAIA?

**A: No.** GitHub Projects is completely optional. GAIA works perfectly with:
- Local dashboard (`scripts/dashboard_server.py`)
- CLI tools (`scripts/project_summary.py`)
- Local NDJSON files (`doc/todo-archive.ndjson`)

### Q: Can I use both local dashboard and GitHub Projects?

**A: Yes!** They complement each other:
- Local dashboard: Fast, offline, full data access
- GitHub Projects: Team collaboration, visual boards, integration with issues

### Q: Does this work with GitHub Free?

**A: Yes.** GitHub Projects V2 is available on all GitHub plans including Free.

### Q: Can I use this with organization projects?

**A: Yes.** The workflow supports both user and organization projects. Just ensure your token has access to the organization.

### Q: Will this create GitHub Issues automatically?

**A: Only when you run the sync agent explicitly.** The workflow only adds *existing* issues to Projects when labeled. You control when issues are created.

## Support

For issues or questions:
1. Check this documentation
2. Review workflow logs in Actions tab
3. Run sync in dry-run mode to debug
4. Check [AGENT_SESSION_WORKFLOW.md](AGENT_SESSION_WORKFLOW.md) for architecture details

---

**Last Updated**: 2026-02-07  
**Status**: ✅ Fully documented and ready to use  
**Integration Type**: Optional, fully functional
