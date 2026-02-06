# GitHub Copilot Local Development Setup

This guide helps you set up GitHub Copilot to work effectively with the GAIA project on your local machine.

## Quick Start (5 Minutes)

### 1. Automated Setup (Recommended)

Run the automated setup script:

```powershell
# From repository root
python scripts/setup_dev_env.py
```

This will:
- ✅ Verify Python 3.10+ is installed
- ✅ Create and configure virtual environment
- ✅ Install all dependencies
- ✅ Set up secrets configuration
- ✅ Create necessary directories
- ✅ Validate GitHub CLI setup

### 2. Load Project Context

Before starting development, load the project context:

```powershell
python scripts/load_context.py
```

This generates a summary of:
- Current session state
- Backlog items
- Recent activity
- Key files to review
- Quick start recommendations

### 3. Health Check

Verify everything is working:

```powershell
python scripts/health_check.py
```

This validates:
- System requirements
- Project configuration
- Essential components

## GitHub Copilot Integration

### Editor Setup

#### Visual Studio Code

1. Install GitHub Copilot extension:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "GitHub Copilot"
   - Install and sign in

2. Configure workspace settings (`.vscode/settings.json`):

```json
{
  "github.copilot.enable": {
    "*": true,
    "plaintext": true,
    "markdown": true,
    "python": true
  },
  "github.copilot.advanced": {
    "debug.overrideEngine": "copilot-chat",
    "inlineSuggest.enable": true
  }
}
```

#### PyCharm / IntelliJ

1. Install GitHub Copilot plugin:
   - Go to Settings → Plugins
   - Search for "GitHub Copilot"
   - Install and restart

2. Sign in with your GitHub account

### Copilot Workspace Configuration

GAIA includes Copilot workspace instructions in `.github/copilot-instructions.md`. This file helps Copilot understand:

- Project architecture and patterns
- Agent workflow conventions
- Event schema and logging patterns
- Integration points (gh, SQLite, NDJSON)
- Development best practices

**No additional setup needed** - Copilot automatically reads these instructions.

## Working with Copilot

### Getting Context-Aware Suggestions

1. **Load context before coding:**
   ```powershell
   python scripts/load_context.py
   ```

2. **Open key files in your editor:**
   - `.github/copilot-instructions.md` - Agent instructions
   - `PLAN.md` - Current implementation plan
   - `.copilot/session_state.json` - Session state
   - Relevant agent files from `agents/`

3. **Use Copilot Chat for questions:**
   - Ask about architecture: "How does the event system work?"
   - Get implementation help: "How do I create a new agent?"
   - Understand patterns: "What's the standard way to append events?"

### Common Copilot Commands

In VS Code Copilot Chat:

- `/explain` - Explain code or concepts
- `/fix` - Suggest fixes for problems
- `/tests` - Generate tests
- `/help` - Show available commands

### Best Practices

#### 1. Keep Context Fresh

Run context loader frequently:

```powershell
python scripts/load_context.py
```

#### 2. Follow Agent Patterns

When creating new agents, use existing ones as templates:

```python
# Copilot will suggest code based on agents/backlog_agent.py pattern
# Just start typing and let it guide you
```

#### 3. Use Inline Comments for Guidance

```python
# Create a new agent that monitors file changes and emits events
# Follow the standard GAIA agent pattern:
# - Parse CLI args with click
# - Execute main action
# - Append event to events.ndjson
```

Copilot will generate code that follows the project conventions.

#### 4. Ask for Explanations

Select any code and use Copilot Chat to ask:
- "What does this agent do?"
- "How does the event flow work here?"
- "What are the parameters for this function?"

## Development Workflow

### 1. Start Your Session

```powershell
# Activate environment and load config
.\scripts\start_session.ps1

# Or just activate venv:
.\.venv\Scripts\Activate.ps1
```

### 2. Check Health

```powershell
python scripts/health_check.py
```

Fix any issues before starting work.

### 3. Load Context

```powershell
python scripts/load_context.py
```

Review the generated summary in `.tmp/context_summary_*.md`.

### 4. Review Current State

Check these files:
- `.copilot/session_state.json` - Where you left off
- `PLAN.md` - Current approved plan
- `TODO.md` - Pending tasks
- `events.ndjson` - Recent activity (tail the file)

### 5. Start Coding with Copilot

Open your editor with Copilot enabled and start working. Copilot will:
- Suggest code based on project patterns
- Auto-complete agent implementations
- Generate event schemas
- Suggest test cases

### 6. Test Frequently

```powershell
# Run specific tests
pytest tests/test_your_feature.py -v

# Run all tests
pytest -v

# Run agents in dry-run mode
$env:PROTOTYPE_USE_LOCAL_EVENTS=1
python agents/your_agent.py --dry-run
```

### 7. Commit and Update State

```powershell
# Commit your work
git add .
git commit -m "feat: your feature description"

# Update session state
# Edit .copilot/session_state.json with your progress
```

## Troubleshooting

### Copilot Not Giving Good Suggestions?

1. **Ensure context files are open:**
   - Open `.github/copilot-instructions.md`
   - Open a reference agent file (e.g., `agents/backlog_agent.py`)
   - Open the file you're working on

2. **Reload window/editor**
   - VS Code: Ctrl+Shift+P → "Developer: Reload Window"

3. **Check Copilot status**
   - Look for Copilot icon in status bar
   - Ensure you're signed in

### Environment Issues?

Run the health check:

```powershell
python scripts/health_check.py
```

Or re-run setup:

```powershell
python scripts/setup_dev_env.py
```

### Need More Context?

Load fresh context:

```powershell
python scripts/load_context.py
```

Read the generated summary file.

## Advanced Tips

### Using Copilot for Backlog Items

1. Load context to see backlog items
2. Pick a task from the summary
3. Ask Copilot Chat:
   ```
   "I need to implement [task description]. 
   Show me how to create an agent for this following GAIA patterns."
   ```

### Generating Proposals

Ask Copilot to help with planning:

```
"Based on the backlog item [X], create an implementation plan 
with steps similar to PLAN.md"
```

### Code Review with Copilot

Before committing:

```
"Review this agent implementation for:
- Correct event schema
- Proper error handling
- GAIA conventions
- Security issues"
```

## Getting Help

### Resources

- **Project README:** `README.md` - Overview and quick start
- **Agent Instructions:** `.github/copilot-instructions.md` - Detailed patterns
- **Session Guide:** `README_SESSION.md` - Session workflows
- **Technical Docs:** `doc/02_technical/` - Architecture details

### Common Questions

**Q: How do I create a new agent?**

A: Use an existing agent as a template. Load `agents/backlog_agent.py` and ask Copilot to help create a similar one.

**Q: How do I test my changes?**

A: Run `pytest` for tests and use `PROTOTYPE_USE_LOCAL_EVENTS=1` for dry-run mode.

**Q: Where do I find the current plan?**

A: Check `PLAN.md` and `.copilot/session_state.json`.

**Q: How do I avoid committing secrets?**

A: Use `.env` for secrets (already in `.gitignore`) or the secrets manager: `python scripts/secrets_cli.py`.

## Next Steps

Now that you're set up:

1. ✅ Run `python scripts/health_check.py` to verify setup
2. ✅ Run `python scripts/load_context.py` to understand current state
3. ✅ Open your editor with Copilot enabled
4. ✅ Review `PLAN.md` and `.copilot/session_state.json`
5. ✅ Start coding with Copilot assistance!

Happy coding with GitHub Copilot and GAIA! 🚀
