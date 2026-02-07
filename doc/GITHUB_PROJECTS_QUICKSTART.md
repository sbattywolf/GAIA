# GitHub Projects Quick Reference

## ✅ Integration Status: IMPLEMENTED

GitHub Projects integration is **fully implemented and ready to use**. This is an optional feature that complements GAIA's local dashboard.

## What You Asked

> "how can i integrate this https://github.com/sbattywolf/GAIA/projects?query=is%3Aopen in gaia or is already done?"

**Answer**: ✅ **Already implemented!** The integration exists and just needs configuration.

## What's Included

### 1. Automatic Issue Addition to Projects
- **File**: `.github/workflows/sprint_onboard.yml`
- **Trigger**: When issues are labeled with `sprint/*`
- **Action**: Automatically adds issue to your GitHub Project board
- **Status**: ✅ Working (requires `PROJECT_V2_NUMBER` secret)

### 2. Database to GitHub Issues Sync
- **File**: `agents/github_sessions_sync.py`
- **Purpose**: Sync `gaia.db` backlog → GitHub Issues
- **Features**: 
  - Dry-run mode for testing
  - Duplicate detection via GAIA_ID tags
  - Priority-based labeling
- **Status**: ✅ Working (requires tokens)

### 3. Documentation
- **File**: `doc/GITHUB_PROJECTS_INTEGRATION.md` (NEW)
- **File**: `doc/AGENT_SESSION_WORKFLOW.md`
- **Status**: ✅ Complete

### 4. Setup Helper
- **File**: `scripts/setup_github_projects.py` (NEW)
- **Purpose**: Check configuration and guide setup
- **Status**: ✅ Working

## Quick Setup (2 minutes)

### Step 1: Check Current Status
```bash
python scripts/setup_github_projects.py check
```

### Step 2: Create GitHub Project
1. Go to: https://github.com/users/sbattywolf/projects
2. Click "New project"
3. Note the project number from URL (e.g., `/projects/1`)

### Step 3: Configure Secret
1. Go to repository Settings → Secrets and variables → Actions
2. Add secret: `PROJECT_V2_NUMBER` = `1` (your project number)
3. Done!

### Step 4: Test
```bash
# Create a test issue
gh issue create --title "Test sprint integration" --label "sprint/test"

# Check your GitHub Project - issue should appear automatically
```

## Usage Examples

### Workflow 1: Manual Issue Management
```bash
# 1. Create issues in GitHub
gh issue create --title "My task" --body "Description"

# 2. Add to current sprint
gh issue edit 123 --add-label "sprint/current"

# 3. Issue appears in GitHub Project automatically
```

### Workflow 2: Sync from Local Database
```bash
# 1. Maintain tasks in gaia.db (or doc/todo-archive.ndjson)

# 2. Preview sync
python agents/github_sessions_sync.py --dry-run

# 3. Sync to GitHub (creates issues)
export AUTOMATION_GITHUB_TOKEN="ghp_your_token"
export AUTOMATION_GITHUB_REPOSITORY="sbattywolf/GAIA"
python agents/github_sessions_sync.py

# 4. Label issues with sprint/* to add to Project
gh issue edit 123 --add-label "sprint/2026-02"
```

### Workflow 3: Combined Local + GitHub
```bash
# 1. View local dashboard
python scripts/dashboard_server.py
# Open: http://localhost:8080/dashboard

# 2. Sync important items to GitHub
python agents/github_sessions_sync.py

# 3. Manage sprint in GitHub Projects UI
# https://github.com/users/sbattywolf/projects/1

# Both views stay in sync!
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Local GAIA System                         │
├─────────────────────────────────────────────────────────────┤
│  • doc/todo-archive.ndjson (tasks)                          │
│  • gaia.db (SQLite database)                                │
│  • Local Dashboard (http://localhost:8080)                  │
│  • CLI tools (project_summary.py, etc.)                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    [Sync Agent]
           (agents/github_sessions_sync.py)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Issues                           │
├─────────────────────────────────────────────────────────────┤
│  • Issues tagged with GAIA_ID                               │
│  • Labeled by priority (gaia:high, etc.)                    │
│  • Created/updated via GitHub API                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
                [Label with sprint/*]
            (manual or via gh CLI)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│               GitHub Projects V2 Board                       │
├─────────────────────────────────────────────────────────────┤
│  • Kanban/Table/Roadmap views                               │
│  • Automatic addition via workflow                          │
│  • Team collaboration features                              │
│  • https://github.com/users/sbattywolf/projects/N           │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

### ✅ Automatic Workflow
- Issues labeled `sprint/*` → Auto-added to Project
- Checklist automatically added to sprint issues
- Works with both user and organization projects

### ✅ Sync Agent
- One-way sync: gaia.db → GitHub Issues
- Dry-run mode for testing
- Duplicate prevention via GAIA_ID tagging
- Priority-based labels

### ✅ Local Dashboard
- Still works independently
- No internet required
- Fast, responsive UI
- Complete data access

### ✅ Combined Power
- Local: Fast iteration, offline work
- GitHub: Team collaboration, visibility
- Best of both worlds!

## Configuration Files

### Required (for auto-add to Projects)
- Repository Secret: `PROJECT_V2_NUMBER`

### Optional (for sync agent)
- Environment: `AUTOMATION_GITHUB_TOKEN`
- Environment: `AUTOMATION_GITHUB_REPOSITORY`

### Workflow File
- `.github/workflows/sprint_onboard.yml` (already configured)

### Sync Agent
- `agents/github_sessions_sync.py` (ready to use)

## Common Tasks

### Check Integration Status
```bash
python scripts/setup_github_projects.py check
```

### Test Sync (Dry-Run)
```bash
python scripts/setup_github_projects.py test
```

### Configure Project Number
```bash
python scripts/setup_github_projects.py configure --project-number 1
```

### Create Sprint Label
```bash
gh label create "sprint/2026-02" --color "0E8A16" --description "Sprint Feb 2026"
```

### Bulk Label Issues
```bash
# Label all issues with "backlog" label as "sprint/current"
gh issue list --label "backlog" --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "sprint/current"
```

### View Project in Browser
```bash
# For user projects
open "https://github.com/users/sbattywolf/projects/1"

# For org projects
open "https://github.com/orgs/YOUR_ORG/projects/1"
```

## Troubleshooting

### Issue: "Project not adding issues"
**Solution**: 
1. Check `PROJECT_V2_NUMBER` secret is set
2. Verify project number in GitHub UI
3. Check workflow logs in Actions tab

### Issue: "Sync agent fails"
**Solution**:
1. Run `python scripts/setup_github_projects.py check`
2. Verify token has `repo` scope
3. Test with `--dry-run` first

### Issue: "Rate limit exceeded"
**Solution**:
1. Check limits: `gh api rate_limit`
2. Wait for reset
3. Use batch operations instead of individual

## Documentation Links

- **Complete Guide**: [GITHUB_PROJECTS_INTEGRATION.md](GITHUB_PROJECTS_INTEGRATION.md)
- **Architecture**: [AGENT_SESSION_WORKFLOW.md](AGENT_SESSION_WORKFLOW.md)
- **Secrets Management**: [SECRETS_MANAGEMENT_GUIDE.md](SECRETS_MANAGEMENT_GUIDE.md)
- **Token Guide**: [GITHUB_2FA_GUIDE.md](GITHUB_2FA_GUIDE.md)

## FAQ

**Q: Is this required?**  
A: No! GitHub Projects is completely optional. GAIA works perfectly with just local tools.

**Q: Does it work offline?**  
A: Local dashboard works offline. GitHub Projects sync requires internet.

**Q: Can I use both?**  
A: Yes! They complement each other. Local for fast work, GitHub for team collaboration.

**Q: What about GitHub Issues?**  
A: Sync agent creates GitHub Issues. Workflow adds Issues to Projects when labeled.

**Q: Does it cost money?**  
A: No! GitHub Projects V2 is free on all plans.

## Support

Need help?
1. Run: `python scripts/setup_github_projects.py check`
2. Read: [GITHUB_PROJECTS_INTEGRATION.md](GITHUB_PROJECTS_INTEGRATION.md)
3. Check workflow logs in Actions tab

---

**TL;DR**: GitHub Projects integration is ✅ **DONE** and ready to use. Just configure `PROJECT_V2_NUMBER` secret and start labeling issues with `sprint/*`.

**Created**: 2026-02-07  
**Status**: ✅ Complete and documented
