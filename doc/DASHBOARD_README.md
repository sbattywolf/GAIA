# GAIA Project Dashboard

A comprehensive web-based dashboard for monitoring and managing the GAIA (Agent-First Backlog Orchestrator) project.

## Features

### 📊 Overview Dashboard
- **Statistics Cards**: Quick metrics showing total tasks, completed work, in-progress items, and critical priorities
- **Progress Tracking**: Visual progress bar showing overall completion percentage
- **Hours Tracking**: Estimated vs actual hours spent across all tasks
- **Recent Updates**: Timeline of latest task changes and updates

### 📋 Task Management
- **Interactive Table**: Sortable and filterable task list
- **Advanced Filters**:
  - Status (pending, in-progress, completed)
  - Priority (critical, high, medium, low)
  - Search by task ID, title, or description
- **Color-Coded Badges**: Visual indicators for status and priority
- **Task Details**: Estimated hours, progress percentage, and last updated timestamps

### 🤖 Agent Status
- **Agent Registry**: List of all configured agents
- **Agent Information**: ID, name, description, version, and model
- **Status Indicators**: Visual markers for active/inactive agents

### 📈 Timeline View
- **Project Timeline**: Visual representation of task progression over time
- **Daily Snapshots**: Historical view of daily progress

## Quick Start

### Prerequisites
- Python 3.10+
- GAIA project repository

### Starting the Dashboard

#### Option 1: Direct Server Start
```bash
cd /home/runner/work/GAIA/GAIA
python scripts/dashboard_server.py --port 8080
```

#### Option 2: Using Test Script
```bash
cd /home/runner/work/GAIA/GAIA
python scripts/test_dashboard.py
```

#### Option 3: Custom Port
```bash
python scripts/dashboard_server.py --host 0.0.0.0 --port 8090
```

### Accessing the Dashboard

Open your web browser and navigate to:
```
http://127.0.0.1:8080/dashboard
```

Or if using a custom port:
```
http://127.0.0.1:<your-port>/dashboard
```

## API Endpoints

The dashboard server provides RESTful API endpoints for accessing project data:

### GET /api/stats
Returns project-wide statistics:
```json
{
  "total_tasks": 35,
  "completed_tasks": 15,
  "pending_tasks": 18,
  "inprogress_tasks": 2,
  "critical_tasks": 3,
  "high_priority_tasks": 8,
  "total_agents": 5,
  "total_est_hours": 120.5,
  "completed_hours": 45.0
}
```

### GET /api/tasks
Returns full list of tasks from `doc/todo-archive.ndjson`:
```json
[
  {
    "id": "T001",
    "title": "Task title",
    "description": "Task description",
    "status": "pending",
    "priority": "high",
    "est_hours": 4.5,
    "added_at": "2026-02-06T12:00:00Z"
  },
  ...
]
```

### GET /api/agents
Returns configured agents from `agents.json`:
```json
[
  {
    "id": "agent-id",
    "name": "Agent Name",
    "description": "Agent description",
    "version": "1.0",
    "model": "gpt-4"
  },
  ...
]
```

### GET /api/pending
Returns pending commands from `.tmp/pending_commands.json`:
```json
{
  "pending": [...]
}
```

## Configuration

### Environment Variables

The dashboard server supports the following environment variables:

- `GAIA_DASHBOARD_HOST`: Host to bind to (default: `127.0.0.1`)
- `GAIA_DASHBOARD_PORT`: Port to bind to (default: `8080`)

Example:
```bash
export GAIA_DASHBOARD_HOST="0.0.0.0"
export GAIA_DASHBOARD_PORT="8090"
python scripts/dashboard_server.py
```

### Command Line Arguments

```bash
python scripts/dashboard_server.py --help

usage: dashboard_server.py [-h] [--host HOST] [--port PORT]

GAIA Project Dashboard Server

options:
  -h, --help   show this help message and exit
  --host HOST  Host to bind to (default: 127.0.0.1)
  --port PORT  Port to bind to (default: 8080)
```

## Data Sources

The dashboard reads data from the following files:

| File | Purpose | Format |
|------|---------|--------|
| `doc/todo-archive.ndjson` | Task tracking and backlog | NDJSON |
| `agents.json` | Agent configurations | JSON |
| `.tmp/pending_commands.json` | Pending commands | JSON |

## Architecture

### Frontend
- **Pure JavaScript**: No external frameworks, vanilla JS for simplicity
- **Responsive CSS**: Mobile-friendly grid layout
- **Auto-refresh**: Updates every 30 seconds
- **Tab Navigation**: Switch between different views seamlessly

### Backend
- **Python HTTP Server**: Lightweight `http.server` based implementation
- **RESTful API**: JSON endpoints for all data
- **Static File Serving**: Serves HTML, CSS, JS, and data files
- **CORS Support**: Allows cross-origin requests for development

## Development

### File Structure
```
scripts/
├── dashboard_server.py      # HTTP server with API endpoints
├── project_dashboard.html   # Main dashboard UI
└── test_dashboard.py        # Testing and development script
```

### Modifying the Dashboard

1. **Edit HTML/CSS/JS**: Modify `scripts/project_dashboard.html`
2. **Add API Endpoints**: Update `scripts/dashboard_server.py`
3. **Test Changes**: Run `python scripts/test_dashboard.py`
4. **Refresh Browser**: Changes to HTML are live, server restart needed for Python changes

### Adding New Views

To add a new view to the dashboard:

1. Add a new nav tab in the HTML:
```html
<button class="nav-tab" onclick="switchView('myview')">🔥 My View</button>
```

2. Add the view content:
```html
<div id="myview" class="view">
  <div class="card">
    <h2>My View</h2>
    <!-- Your content here -->
  </div>
</div>
```

3. Add update function in JavaScript:
```javascript
function updateMyView() {
  // Fetch and display data
}
```

4. Call it in `updateDashboard()`:
```javascript
function updateDashboard() {
  updateOverview();
  updateTasksTable();
  updateAgentsList();
  updateMyView();  // Add your function
}
```

## Troubleshooting

### Port Already in Use
If you see `OSError: [Errno 98] Address already in use`:

1. Find the process using the port:
```bash
lsof -ti:8080
```

2. Kill the process:
```bash
kill <PID>
```

3. Start the server again

### No Data Showing
If the dashboard shows no tasks or agents:

1. Check that data files exist:
```bash
ls -la doc/todo-archive.ndjson agents.json
```

2. Verify file format:
```bash
head -2 doc/todo-archive.ndjson
```

3. Check server logs for errors

### API Not Responding
1. Verify server is running:
```bash
curl http://127.0.0.1:8080/api/stats
```

2. Check firewall settings
3. Try accessing from localhost vs 0.0.0.0

## Future Enhancements

Planned features for future versions:

- [ ] **Charts**: D3.js or Chart.js integration for visual analytics
- [ ] **Real-time Updates**: WebSocket support for live updates
- [ ] **Authentication**: Token-based auth for API access
- [ ] **Export**: Download tasks as CSV/JSON/PDF
- [ ] **Filtering**: Advanced query builder
- [ ] **Dark Mode**: Theme switcher
- [ ] **Notifications**: Browser notifications for task updates
- [ ] **Mobile App**: Progressive Web App (PWA) support

## Contributing

When contributing to the dashboard:

1. Test all views work correctly
2. Ensure responsive design on mobile
3. Maintain consistent styling
4. Document any new API endpoints
5. Update this README with new features

## License

Part of the GAIA project. See main repository for license information.

## Support

For issues or questions about the dashboard:
1. Check this README
2. Review existing GitHub issues
3. Create a new issue with details about your problem

---

**Version**: 1.0  
**Last Updated**: 2026-02-07  
**Maintainer**: GAIA Team
