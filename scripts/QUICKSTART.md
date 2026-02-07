# GAIA Dashboard - Quick Start Guide

Get up and running with the GAIA project dashboard in 60 seconds.

## 🚀 Quick Start

### 1. Start the Dashboard

```bash
cd /home/runner/work/GAIA/GAIA
python scripts/dashboard_server.py --port 8080
```

You should see:
```
🚀 GAIA Project Dashboard serving on http://127.0.0.1:8080
   Access the dashboard at: http://127.0.0.1:8080/dashboard
   Press CTRL+C to stop
```

### 2. Open in Browser

Navigate to: **http://127.0.0.1:8080/dashboard**

### 3. Explore the Views

- Click **📊 Overview** - See project statistics and progress
- Click **📋 Tasks** - View and filter all tasks
- Click **🤖 Agents** - Check agent status
- Click **📈 Timeline** - View project timeline

## 📊 Alternative: CLI Summary

For a quick command-line summary:

```bash
python scripts/project_summary.py
```

Output:
```
============================================================
  🚀 GAIA PROJECT SUMMARY
============================================================
  Total Tasks............................. 35
  Completed............................... 6 (17.1%)
  ...
```

## 🔧 Configuration

### Change Port

```bash
python scripts/dashboard_server.py --port 9000
```

### Allow External Access

```bash
python scripts/dashboard_server.py --host 0.0.0.0 --port 8080
```

Then access from other machines at: `http://YOUR_IP:8080/dashboard`

### Use Environment Variables

```bash
export GAIA_DASHBOARD_PORT=8090
python scripts/dashboard_server.py
```

## 📖 Full Documentation

For complete documentation, see:
- [`doc/DASHBOARD_README.md`](../doc/DASHBOARD_README.md) - Full usage guide
- [`doc/PROJECT_VIEWS_SUMMARY.md`](../doc/PROJECT_VIEWS_SUMMARY.md) - Implementation details

## 🆘 Troubleshooting

### Port Already in Use?

```bash
# Find process using port 8080
lsof -ti:8080

# Kill it (replace PID with actual number)
kill <PID>

# Try again
python scripts/dashboard_server.py --port 8080
```

### Dashboard Not Loading?

1. Check server is running: Look for startup message
2. Verify URL: Make sure you're using `/dashboard` at the end
3. Check firewall: Ensure port is not blocked

### No Data Showing?

1. Verify data files exist:
   ```bash
   ls -la doc/todo-archive.ndjson agents.json
   ```

2. Check file contents:
   ```bash
   head -2 doc/todo-archive.ndjson
   ```

## 🎯 What You Can Do

### In the Dashboard
- ✅ View real-time project statistics
- ✅ Filter tasks by status and priority
- ✅ Search for specific tasks
- ✅ Monitor agent configurations
- ✅ Track project progress

### Using the CLI
- ✅ Get quick project overview
- ✅ See priority breakdown
- ✅ Track time spent vs estimated
- ✅ View recent activity

## 📊 Current Data

The dashboard displays live data from:
- **35 tasks** tracked in `doc/todo-archive.ndjson`
- **5 agents** configured in `agents.json`
- **191 hours** of estimated work
- **17.1%** completion rate

## 🔗 API Access

The dashboard provides RESTful APIs:

```bash
# Get statistics
curl http://127.0.0.1:8080/api/stats

# Get all tasks
curl http://127.0.0.1:8080/api/tasks

# Get agents
curl http://127.0.0.1:8080/api/agents
```

## 💡 Tips

1. **Auto-refresh**: Dashboard updates every 30 seconds automatically
2. **Filters**: Combine status, priority, and search filters for precise results
3. **CLI**: Use `project_summary.py` for quick checks without starting server
4. **Mobile**: Dashboard is responsive and works on phones/tablets

## 📧 Need Help?

- Check [`doc/DASHBOARD_README.md`](../doc/DASHBOARD_README.md) for detailed docs
- Review [`doc/PROJECT_VIEWS_SUMMARY.md`](../doc/PROJECT_VIEWS_SUMMARY.md) for technical details
- Look at inline code comments for implementation details

---

**Ready to explore your project data!** 🎉

Start with: `python scripts/dashboard_server.py --port 8080`
