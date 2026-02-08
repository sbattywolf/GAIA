# Dashboard Refresh Options

The GAIA dashboard provides multiple ways to refresh the `doc/todo-archive.ndjson` data from source files.

## 1. Manual Refresh Button (Recommended for Interactive Use)

The dashboard includes a **"Refresh Archive"** button in the top-right corner that triggers the `update_todo_archive.py` script on-demand.

### How It Works
- Click the 🔄 **Refresh Archive** button
- The script consolidates data from `sprints/*.json`, `backlogs/*.json`, and `tasks.json`
- A success/error message appears showing the results
- The dashboard automatically reloads the updated data

### API Endpoint
- **Endpoint**: `POST /api/refresh`
- **Response**: JSON with `success`, `message`, `output`, and `stats`

```bash
# Test the API endpoint directly
curl -X POST http://localhost:9080/api/refresh
```

## 2. Automatic Dashboard Refresh (Already Enabled)

The dashboard automatically refreshes the **displayed data** every 30 seconds.

**Note**: This only refreshes what's displayed from existing files, it does NOT consolidate source files. Use the manual refresh button or scheduler to update the archive from sources.

### Configuration
Edit `scripts/project_dashboard.html` line ~800:
```javascript
// Auto-refresh every 30 seconds (default)
setInterval(loadData, 30000);

// To change interval (e.g., every 60 seconds):
setInterval(loadData, 60000);
```

## 3. Scheduled Refresh (Command Line)

Use cron (Linux/Mac) or Task Scheduler (Windows) to run the update script periodically.

### Linux/Mac (cron)
```bash
# Edit crontab
crontab -e

# Add line to run every 5 minutes
*/5 * * * * cd /path/to/GAIA && python scripts/update_todo_archive.py

# Run every hour
0 * * * * cd /path/to/GAIA && python scripts/update_todo_archive.py

# Run daily at 2 AM
0 2 * * * cd /path/to/GAIA && python scripts/update_todo_archive.py
```

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Name: "GAIA Archive Update"
4. Trigger: Select frequency (e.g., Daily, Hourly)
5. Action: Start a program
   - Program: `python`
   - Arguments: `scripts\update_todo_archive.py`
   - Start in: `C:\path\to\GAIA`

### Using Python APScheduler
Create a scheduler script:

```python
# scripts/archive_scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'update_todo_archive.py'

def update_archive():
    """Run the update script."""
    print("Running archive update...")
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✓ Archive updated successfully")
    else:
        print(f"✗ Update failed: {result.stderr}")

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # Run every 5 minutes
    scheduler.add_job(update_archive, 'interval', minutes=5)
    print("Archive scheduler started (every 5 minutes)")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Scheduler stopped")
```

Run it:
```bash
pip install apscheduler
python scripts/archive_scheduler.py
```

## 4. File Watcher (Advanced - Automatic on Changes)

For automatic updates when source files change, use a file watcher:

```python
# scripts/archive_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'update_todo_archive.py'

class ArchiveUpdateHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_update = 0
        self.cooldown = 5  # seconds between updates
    
    def on_modified(self, event):
        # Check if a sprint or backlog JSON was modified
        if event.src_path.endswith('.json'):
            if 'sprints/' in event.src_path or 'backlogs/' in event.src_path:
                now = time.time()
                if now - self.last_update > self.cooldown:
                    print(f"File changed: {event.src_path}")
                    print("Updating archive...")
                    subprocess.run([sys.executable, str(SCRIPT)])
                    self.last_update = now

if __name__ == '__main__':
    observer = Observer()
    handler = ArchiveUpdateHandler()
    
    # Watch sprints and backlogs directories
    observer.schedule(handler, str(ROOT / 'sprints'), recursive=False)
    observer.schedule(handler, str(ROOT / 'backlogs'), recursive=False)
    
    print("File watcher started...")
    print("Watching: sprints/*.json, backlogs/*.json")
    print("Press Ctrl+C to stop")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

Install and run:
```bash
pip install watchdog
python scripts/archive_watcher.py
```

## Comparison

| Method | When to Use | Pros | Cons |
|--------|-------------|------|------|
| **Manual Button** | Interactive sessions, on-demand updates | Easy, visible, immediate feedback | Requires user action |
| **Auto Display Refresh** | Always (already enabled) | Seamless, no action needed | Only refreshes display, not source consolidation |
| **Cron/Scheduler** | Production, unattended | Reliable, set-and-forget | Fixed schedule, may run unnecessarily |
| **File Watcher** | Development, immediate sync | Updates only when needed | Requires running process, more complex |

## Recommendations

### For Development
- Use **Manual Button** when actively working
- Optional: Run **File Watcher** for automatic updates

### For Production
- Use **Cron/Scheduler** to run every 5-15 minutes
- Keep **Auto Display Refresh** enabled (default 30s)

### For CI/CD
- Run `update_todo_archive.py` in build/deployment pipeline
- Sync to database with `agents/sync_backlog_to_db.py`

## Troubleshooting

### Button doesn't work
- Check browser console for errors (F12)
- Verify server is running: `curl http://localhost:9080/api/refresh -X POST`
- Check server logs for errors

### Scheduler not running
- Verify cron syntax: `crontab -l`
- Check cron logs: `/var/log/syslog` or `journalctl -u cron`
- Ensure full paths are used in cron commands

### File watcher not detecting changes
- Verify watchdog is installed: `pip show watchdog`
- Check that directories exist: `sprints/`, `backlogs/`
- Some editors use atomic writes (create temp file, rename) which may not trigger events

## See Also
- [UPDATE_TODO_ARCHIVE_README.md](UPDATE_TODO_ARCHIVE_README.md) - Script documentation
- [LAPTOP_SETUP.md](../LAPTOP_SETUP.md) - Dashboard setup guide
