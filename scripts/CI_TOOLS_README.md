# CI Issue Management Tools

This directory contains scripts for managing CI/CD issues and workflow failures in the GAIA repository.

## Scripts

### ci_issue_manager.py

**Purpose:** Comprehensive CI issue collection, classification, and management tool.

**Features:**
- Fetches failed workflow runs from GitHub Actions
- Classifies failures by type (security, test, build, integration) and urgency (critical, high, medium, low)
- Identifies duplicate issues
- Verifies if issues are fixed by checking recent successful runs
- Closes fixed issues with verification comments
- Creates new issues for unfixed failures
- Generates detailed JSON reports

**Usage:**

```bash
# Using GitHub MCP (when gh CLI not available)
python3 scripts/ci_issue_manager.py \
  --runs-file /tmp/workflow_runs.json \
  --issues-file /tmp/issues.json \
  --dry-run

# Using gh CLI (when available with GH_TOKEN)
python3 scripts/ci_issue_manager.py \
  --use-gh \
  --limit 100 \
  --dry-run
```

**Options:**
- `--repo`: Repository in format owner/repo (default: sbattywolf/GAIA)
- `--dry-run`: Don't make changes, just generate report
- `--limit`: Number of workflow runs to fetch (default: 100)
- `--runs-file`: Load workflow runs from JSON file
- `--issues-file`: Load issues from JSON file
- `--use-gh`: Use gh CLI to fetch data

**Output:**
- Console summary of findings
- `ci_issues_report.json`: Detailed JSON report with all analysis

---

### close_fixed_issues.py

**Purpose:** Automatically close CI issues that have been resolved.

**Features:**
- Fetches open CI issues by label
- Extracts workflow run information from issue bodies
- Checks if subsequent workflow runs succeeded
- Closes issues with verification comments

**Usage:**

```bash
# Dry run to see what would be closed
python3 scripts/close_fixed_issues.py --dry-run

# Actually close fixed issues
python3 scripts/close_fixed_issues.py

# Custom options
python3 scripts/close_fixed_issues.py \
  --repo sbattywolf/GAIA \
  --label "ci-failure,needs-triage" \
  --max-issues 50
```

**Options:**
- `--repo`: Repository in format owner/repo (default: sbattywolf/GAIA)
- `--dry-run`: Don't make changes, just report what would be done
- `--label`: Comma-separated list of labels to filter (default: ci-failure,needs-triage)
- `--max-issues`: Maximum number of issues to check (default: 50)

**Note:** Requires `gh` CLI with valid authentication.

---

### fetch_ci_data.py

**Purpose:** Template script for fetching CI data using GitHub API.

This is a helper template when working in environments without gh CLI. In practice, you should use GitHub MCP server tools or the GitHub API directly to fetch:
- Workflow runs data → save to `/tmp/workflow_runs.json`
- Issues data → save to `/tmp/issues.json`

---

## CI Issues Analysis Document

See `CI_ISSUES_ANALYSIS.md` in the repository root for a comprehensive analysis of all current CI failures, including:
- Classification by urgency and type
- Root cause analysis
- Actionable recommendations
- Fix priorities and timelines

---

## Workflow Integration

These scripts are designed to be integrated into GitHub Actions workflows for automated CI triage. Example workflow:

```yaml
name: Automated CI Triage

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch: {}

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run CI Issue Manager
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/ci_issue_manager.py --use-gh --dry-run
      
      - name: Close Fixed Issues
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/close_fixed_issues.py
```

---

## Development

### Adding New Classification Rules

Edit `ci_issue_manager.py`, function `classify_failure()`:

```python
def classify_failure(self, run: Dict) -> Dict[str, str]:
    workflow_name = run.get('name', '')
    path = run.get('path', '')
    
    # Add your classification logic here
    if 'your-pattern' in workflow_name.lower():
        failure_type = 'your-type'
        urgency = 'high'
    
    # ...
```

### Testing

Always use `--dry-run` first to verify behavior before making actual changes:

```bash
python scripts/ci_issue_manager.py --runs-file /tmp/test_runs.json --issues-file /tmp/test_issues.json --dry-run
```

---

## Troubleshooting

### "gh CLI not available"

When running without gh CLI (e.g., in GitHub Copilot environment):
1. Use GitHub MCP tools to fetch data manually
2. Save to JSON files
3. Use `--runs-file` and `--issues-file` options

### "Error running gh command"

Check that `GH_TOKEN` or `GITHUB_TOKEN` environment variable is set:

```bash
export GH_TOKEN="your-token"
# or
export GITHUB_TOKEN="${{ secrets.GITHUB_TOKEN }}"
```

### No issues being closed

Check:
1. Issue labels match the filter (default: `ci-failure,needs-triage`)
2. Workflow names can be extracted from issue bodies
3. Recent workflow runs exist for comparison

---

## Contributing

When adding new CI management features:
1. Follow the existing code patterns
2. Add comprehensive error handling
3. Support both dry-run and live modes
4. Document usage in this README
5. Test with `--dry-run` first

---

*Last updated: 2026-02-05*
