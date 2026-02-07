# Running GAIA Dashboard on Your Laptop

**YES! This dashboard runs perfectly on your laptop.** Here's everything you need to know.

## 🖥️ What You're Getting

The GAIA dashboard is a **local web application** that runs entirely on your computer. It:
- ✅ Runs on Windows, Mac, or Linux
- ✅ Requires only Python (no external dependencies)
- ✅ Reads data from local files in this repository
- ✅ Starts a local web server on your machine
- ✅ Opens in your web browser at `http://localhost:9080`

**Important**: This dashboard shows data from the local `doc/todo-archive.ndjson` file in this repository, **NOT** from GitHub Projects API.

## ⚡ Super Quick Start (3 Steps)

### Step 1: Check You Have Python

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:

```bash
python --version
```

or try:

```bash
python3 --version
```

You need **Python 3.10 or higher**. If you don't have it, download from [python.org](https://www.python.org/downloads/).

### Step 2: Navigate to the Repository

```bash
cd /path/to/GAIA
```

Replace `/path/to/GAIA` with wherever you cloned this repository.

### Step 3: Start the Dashboard

```bash
python scripts/dashboard_server.py --port 9080
```

or on some systems:

```bash
python3 scripts/dashboard_server.py --port 9080
```

You should see:
```
🚀 GAIA Project Dashboard serving on http://127.0.0.1:9080
   Access the dashboard at: http://127.0.0.1:9080/dashboard
   Press CTRL+C to stop
```

### Step 4: Open Your Browser

Open any web browser and go to:
```
http://localhost:9080/dashboard
```

or:
```
http://127.0.0.1:9080/dashboard
```

That's it! You should see the dashboard.

## 🔍 Detailed Setup Instructions

### For Windows Users

1. **Check Python Installation**
   - Open Command Prompt (search "cmd" in Start menu)
   - Type: `python --version`
   - If not installed, download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Navigate to Repository**
   ```cmd
   cd C:\Users\YourName\Documents\GAIA
   ```

3. **Start Dashboard**
   ```cmd
   python scripts\dashboard_server.py --port 9080
   ```

4. **Open Browser**
   - Open Chrome, Firefox, or Edge
   - Go to: `http://localhost:9080/dashboard`

5. **Stop Dashboard**
   - Press `Ctrl+C` in the Command Prompt window

### For Mac Users

1. **Check Python Installation**
   - Open Terminal (Applications → Utilities → Terminal)
   - Type: `python3 --version`
   - If not installed, download from [python.org](https://www.python.org/downloads/)
   - Or use Homebrew: `brew install python3`

2. **Navigate to Repository**
   ```bash
   cd ~/Documents/GAIA
   ```

3. **Start Dashboard**
   ```bash
   python3 scripts/dashboard_server.py --port 9080
   ```

4. **Open Browser**
   - Open Safari, Chrome, or Firefox
   - Go to: `http://localhost:9080/dashboard`

5. **Stop Dashboard**
   - Press `Ctrl+C` in the Terminal window

### For Linux Users

1. **Check Python Installation**
   ```bash
   python3 --version
   ```
   - If not installed: `sudo apt install python3` (Ubuntu/Debian)
   - Or: `sudo yum install python3` (RedHat/CentOS)

2. **Navigate to Repository**
   ```bash
   cd ~/GAIA
   ```

3. **Start Dashboard**
   ```bash
   python3 scripts/dashboard_server.py --port 9080
   ```

4. **Open Browser**
   - Go to: `http://localhost:9080/dashboard`

5. **Stop Dashboard**
   - Press `Ctrl+C` in the terminal

## 🎯 What Data Does It Show?

The dashboard displays data from **local files** in this repository:

| File | Contains | Location |
|------|----------|----------|
| `doc/todo-archive.ndjson` | All tasks and their status | `doc/` folder |
| `agents.json` | Agent configurations | Root folder |
| `.tmp/pending_commands.json` | Pending commands (optional) | `.tmp/` folder |

**It does NOT connect to:**
- ❌ GitHub Projects API
- ❌ GitHub Issues
- ❌ Any external services
- ❌ The internet (runs completely offline)

If you want to see **YOUR** tasks in the dashboard:
1. Add your tasks to `doc/todo-archive.ndjson` (one JSON object per line)
2. Refresh the dashboard in your browser

## 🚨 Troubleshooting

### "Command not found: python"

**Problem**: Python is not installed or not in your PATH.

**Solution**:
- Windows: Reinstall Python and check "Add to PATH"
- Mac: Use `python3` instead of `python`
- Linux: Install with your package manager

### "Address already in use"

**Problem**: Port 9080 is being used by another program.

**Solution**: Use a different port:
```bash
python scripts/dashboard_server.py --port 9000
```

Then go to: `http://localhost:9000/dashboard`

### "No data showing in dashboard"

**Problem**: Data files are missing or empty.

**Solution**: Check that these files exist:
```bash
ls doc/todo-archive.ndjson
ls agents.json
```

If `todo-archive.ndjson` is empty, you can add sample data:
```json
{"id":"T001","title":"Sample Task","status":"pending","priority":"high","est_hours":2}
```

### "Browser shows 404 Not Found"

**Problem**: Wrong URL.

**Solution**: Make sure you're using `/dashboard` at the end:
- ✅ Correct: `http://localhost:9080/dashboard`
- ❌ Wrong: `http://localhost:9080`

### "Permission Denied"

**Problem**: Port 9080 requires admin access on some systems.

**Solution**: Use a higher port number:
```bash
python scripts/dashboard_server.py --port 8888
```

## 🔧 Alternative: CLI Tool

If you don't want to use the web dashboard, there's a **command-line tool**:

```bash
python scripts/project_summary.py
```

This shows the same statistics in your terminal, no web browser needed.

## 📱 Can I Access It From My Phone?

Yes! If your laptop and phone are on the same WiFi network:

1. Find your laptop's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr`

2. Start the dashboard allowing external access:
   ```bash
   python scripts/dashboard_server.py --host 0.0.0.0 --port 9080
   ```

3. On your phone, open browser and go to:
   ```
   http://YOUR_LAPTOP_IP:9080/dashboard
   ```
   For example: `http://192.168.1.100:9080/dashboard`

## ❓ Frequently Asked Questions

### Does this connect to GitHub Projects?

**No.** The dashboard reads from local files in your repository. If you want to sync with GitHub Projects, you'd need to:
1. Export your GitHub Projects data
2. Convert it to NDJSON format
3. Save it to `doc/todo-archive.ndjson`

### Do I need to install any packages?

**No.** The dashboard uses only Python's standard library. No `pip install` needed.

### Can I run this on multiple computers?

**Yes.** Just clone the repository on each computer and run the dashboard. Each instance is independent.

### Can I customize the port?

**Yes.** Use `--port` flag:
```bash
python scripts/dashboard_server.py --port 3000
```

### How do I stop the dashboard?

Press `Ctrl+C` in the terminal window where it's running.

### Does it save any data?

**No.** The dashboard only reads data. It doesn't modify or save anything.

## 🎓 Next Steps

Once you have the dashboard running:

1. **Explore the Views**:
   - Overview: See project statistics
   - Tasks: Filter and search all tasks
   - Agents: View agent configurations
   - Timeline: Project timeline (framework)

2. **Try the CLI Tool**:
   ```bash
   python scripts/project_summary.py
   ```

3. **Read the Docs**:
   - [QUICKSTART.md](scripts/QUICKSTART.md) - 60-second guide
   - [DASHBOARD_README.md](doc/DASHBOARD_README.md) - Complete documentation
   - [PROJECT_VIEWS_SUMMARY.md](doc/PROJECT_VIEWS_SUMMARY.md) - Technical details

## 💡 Summary

- ✅ **Yes, runs on your laptop** (Windows, Mac, Linux)
- ✅ **Only needs Python 3.10+** (no other dependencies)
- ✅ **Completely local** (no internet connection needed)
- ✅ **Shows local file data** (not GitHub Projects)
- ✅ **Simple to start** (`python scripts/dashboard_server.py`)
- ✅ **Access in browser** (`http://localhost:9080/dashboard`)

**You're ready to go!** Just run the command and open your browser. 🚀

## 🆘 Still Having Issues?

1. Run the verification script:
   ```bash
   python scripts/verify_setup.py
   ```

2. Check the [Troubleshooting section](#-troubleshooting) above

3. Review [DASHBOARD_README.md](doc/DASHBOARD_README.md)

4. Open an issue on GitHub with:
   - Your operating system
   - Python version (`python --version`)
   - Error message you're seeing
