#!/usr/bin/env python3
"""
Helper script to fetch CI data using direct API calls and save to files.
This is used when gh CLI is not available (like in this environment).
"""

import json
import sys

# Since we can't use gh CLI, we'll create this as a template
# The actual data will be fetched using the GitHub MCP tools externally

def create_template():
    """Create template files."""
    workflow_runs_template = {
        "total_count": 0,
        "workflow_runs": []
    }
    
    issues_template = {
        "issues": []
    }
    
    print("This script is a template for data fetching.")
    print("Use GitHub MCP tools to fetch data and save to:")
    print("  - /tmp/workflow_runs.json")
    print("  - /tmp/issues.json")
    print()
    print("Then run: python3 scripts/ci_issue_manager.py --runs-file /tmp/workflow_runs.json --issues-file /tmp/issues.json --dry-run")

if __name__ == "__main__":
    create_template()
