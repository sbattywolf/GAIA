# GAIA Enhanced Dashboard - Multi-View Project Management

The GAIA Enhanced Dashboard provides multiple perspectives on your project data through specialized views optimized for different workflows and use cases.

## Quick Start

### Start the Server
```bash
cd /home/runner/work/GAIA/GAIA
python scripts/dashboard_server.py --port 9080
```

### Access Dashboards
- **Standard Dashboard**: http://127.0.0.1:9080/dashboard
- **Enhanced Dashboard**: http://127.0.0.1:9080/enhanced (NEW!)

## Available Views

### 📊 1. Overview Dashboard
**Purpose**: High-level project health at a glance

**Features**:
- Key metrics cards (total, completed, in-progress, critical tasks)
- Overall progress bar with hour tracking
- Priority breakdown visualization
- Status distribution chart

**Best for**: Daily standups, stakeholder updates, quick health checks

---

### 📋 2. Kanban Board
**Purpose**: Visual workflow management with drag-and-drop interface

**Features**:
- Three-column layout: Pending → In Progress → Completed
- Task cards with priority badges
- Estimated hours display
- Real-time count of tasks per column

**Best for**: Sprint planning, workflow visualization, team collaboration

**Columns**:
- **Pending (📝)**: Backlog items ready to start
- **In Progress (🚀)**: Active work items
- **Completed (✅)**: Done tasks

---

### 🗺️ 3. Roadmap View
**Purpose**: Strategic planning and milestone tracking

**Features**:
- Timeline-based milestone display
- Grouped tasks by sprint/milestone
- Status and priority indicators for each task
- Expandable task lists per milestone

**Best for**: Long-term planning, sprint reviews, release planning

**Data Organization**:
- Tasks grouped by `sprint` or `milestone` field
- Ungrouped tasks appear in "Backlog"
- Shows total task count per milestone

---

### 📈 4. Gantt Timeline
**Purpose**: Visual project timeline with progress tracking

**Features**:
- Horizontal bar chart showing task progress
- Real-time progress percentage
- Up to 20 tasks displayed (most recent/active)
- Color-coded completion bars

**Best for**: Progress tracking, deadline management, timeline visualization

**Progress Indicators**:
- 0-49%: Red/Orange (needs attention)
- 50-99%: Blue (in progress)
- 100%: Green (completed)

---

### 📅 5. Calendar View
**Purpose**: Deadline and event tracking

**Features**:
- Monthly calendar grid
- Tasks displayed on deadline dates
- Navigation (previous/next month, today)
- Overflow indicator ("+N more" when > 3 tasks/day)

**Best for**: Deadline tracking, planning, scheduling

**Navigation**:
- **← Previous**: Go to previous month
- **Today**: Jump to current month
- **Next →**: Go to next month

**Notes**:
- Uses `deadline` or `target_date` field from tasks
- Shows up to 3 tasks per day with overflow count
- Hover for full task titles

---

### 📊 6. Metrics Dashboard
**Purpose**: Analytics and data visualization

**Features**:
- Task completion trend chart
- Priority distribution pie chart
- Hours breakdown by status
- Velocity trend analysis

**Best for**: Retrospectives, performance analysis, data-driven decisions

**Charts** (Coming Soon):
- **Completion Trend**: Tasks completed over time
- **Priority Distribution**: Visual breakdown of task priorities
- **Hours by Status**: Time allocation across statuses
- **Velocity Trend**: Team velocity tracking

---

## API Endpoints

The enhanced dashboard uses these API endpoints:

### Core Endpoints

#### GET /api/tasks
Returns all tasks from `doc/todo-archive.ndjson`

**Response**:
```json
[
  {
    "id": "T001",
    "title": "Task title",
    "status": "pending",
    "priority": "high",
    "est_hours": 4.5,
    "sprint": "Sprint 1",
    "deadline": "2026-02-15"
  }
]
```

#### GET /api/stats
Project-wide statistics

**Response**:
```json
{
  "total_tasks": 35,
  "completed_tasks": 15,
  "pending_tasks": 18,
  "inprogress_tasks": 2,
  "critical_tasks": 3,
  "total_est_hours": 120.5,
  "completed_hours": 45.0
}
```

#### GET /api/agents
Agent configurations from `agents.json`

#### GET /api/pending
Pending commands from `.tmp/pending_commands.json`

### Enhanced Endpoints (NEW)

#### GET /api/roadmap
Tasks grouped by sprint/milestone

**Response**:
```json
{
  "Sprint 1": [/* tasks */],
  "Sprint 2": [/* tasks */],
  "Backlog": [/* tasks */]
}
```

#### GET /api/sprints
Sprint summary data

**Response**:
```json
[
  {
    "name": "Sprint 1",
    "total_tasks": 10,
    "completed": 5,
    "in_progress": 3,
    "pending": 2
  }
]
```

---

## Data Requirements

### Task Fields

For best results, include these fields in your tasks:

**Required**:
- `id`: Unique task identifier (e.g., "T001")
- `title`: Task description
- `status`: One of "pending", "in-progress", "completed"

**Recommended**:
- `priority`: One of "critical", "high", "medium", "low"
- `est_hours`: Estimated hours (number)
- `progress`: Completion percentage (0-100)

**Optional (for enhanced features)**:
- `sprint`: Sprint name (for roadmap grouping)
- `milestone`: Milestone name (alternative to sprint)
- `deadline`: Due date (ISO 8601 format)
- `target_date`: Alternative to deadline
- `description`: Detailed description
- `added_at`: Creation timestamp
- `last_updated`: Last modification timestamp

### Example Task
```json
{
  "id": "T042",
  "title": "Implement user authentication",
  "description": "Add OAuth2 login flow",
  "status": "in-progress",
  "priority": "high",
  "est_hours": 8,
  "progress": 60,
  "sprint": "Sprint 2",
  "deadline": "2026-02-20T17:00:00Z",
  "added_at": "2026-02-01T09:00:00Z",
  "last_updated": "2026-02-07T14:30:00Z"
}
```

---

## View Selection Guide

### When to Use Each View

| Need | Use This View | Why |
|------|---------------|-----|
| Quick status check | Overview | Fast metrics and progress |
| Sprint planning | Kanban | Visual workflow management |
| Release planning | Roadmap | Milestone and sprint organization |
| Progress tracking | Gantt Timeline | Visual progress bars |
| Deadline management | Calendar | Date-based task view |
| Performance analysis | Metrics | Charts and analytics |

### Workflow Examples

#### Daily Standup
1. **Overview** - Check overall progress
2. **Kanban** - Review in-progress tasks
3. **Calendar** - Note upcoming deadlines

#### Sprint Planning
1. **Roadmap** - Review current sprint status
2. **Kanban** - Organize backlog
3. **Gantt Timeline** - Check task dependencies

#### Monthly Review
1. **Metrics** - Analyze completion trends
2. **Roadmap** - Review milestone progress
3. **Overview** - Share high-level stats

---

## Customization

### Adding Custom Views

To add a new view to the enhanced dashboard:

1. **Add Navigation Tab** (HTML):
```html
<button class="nav-tab" onclick="switchView('myview')">🔥 My View</button>
```

2. **Add View Container** (HTML):
```html
<div id="myview" class="view">
  <div class="card">
    <h2>My View</h2>
    <!-- Your content here -->
  </div>
</div>
```

3. **Add Update Function** (JavaScript):
```javascript
function updateMyView() {
  // Fetch and render data
  const data = allTasks.filter(/* your logic */);
  document.getElementById('myview-content').innerHTML = renderData(data);
}
```

4. **Call in updateDashboard()**:
```javascript
function updateDashboard() {
  updateOverview();
  updateKanban();
  // ... other views
  updateMyView();  // Add your function
}
```

### Styling Custom Views

Use these CSS classes for consistency:

- `.card` - White card container
- `.stat-card` - Metric card with hover effect
- `.badge` - Status/priority badge
- `.kanban-card` - Card in kanban board
- `.timeline-row` - Row in Gantt timeline

---

## Configuration

### Environment Variables
```bash
export GAIA_DASHBOARD_HOST="0.0.0.0"  # Bind to all interfaces
export GAIA_DASHBOARD_PORT="8080"      # Custom port
```

### Command Line
```bash
python scripts/dashboard_server.py --host 0.0.0.0 --port 8080
```

### Auto-Refresh
The dashboard auto-refreshes every 30 seconds. To change:

Edit `project_dashboard_enhanced.html`:
```javascript
// Change 30000 (30 seconds) to your preferred interval
setInterval(loadData, 30000);
```

---

## Performance Tips

### Large Datasets
- Kanban shows all tasks per column (can be slow with 100+ tasks)
- Gantt Timeline limits to 20 tasks by default
- Calendar shows all tasks with deadlines

**Optimization strategies**:
1. Filter tasks by date range before rendering
2. Implement pagination for large task lists
3. Use virtual scrolling for long lists
4. Cache computed data

### Network Optimization
- Dashboard caches task data between view switches
- API calls only made on page load and refresh
- Consider adding service worker for offline support

---

## Troubleshooting

### Common Issues

#### "No tasks showing"
**Cause**: Empty or missing `doc/todo-archive.ndjson`

**Solution**:
```bash
# Check file exists
ls -la doc/todo-archive.ndjson

# Verify format (should be NDJSON)
head -1 doc/todo-archive.ndjson | python -m json.tool
```

#### "Roadmap shows only Backlog"
**Cause**: Tasks missing `sprint` or `milestone` field

**Solution**: Add sprint field to tasks:
```json
{"id": "T001", "title": "...", "sprint": "Sprint 1", ...}
```

#### "Calendar empty"
**Cause**: Tasks missing `deadline` or `target_date` field

**Solution**: Add deadline field:
```json
{"id": "T001", "title": "...", "deadline": "2026-02-20", ...}
```

#### "Enhanced dashboard not loading"
**Cause**: File not found or server not serving it

**Solution**:
```bash
# Check file exists
ls scripts/project_dashboard_enhanced.html

# Restart server
python scripts/dashboard_server.py
```

---

## Comparison: Standard vs Enhanced

| Feature | Standard | Enhanced |
|---------|----------|----------|
| Overview metrics | ✅ | ✅ |
| Task table | ✅ | ❌ |
| Kanban board | ❌ | ✅ |
| Roadmap | ❌ | ✅ |
| Gantt timeline | Basic | Enhanced |
| Calendar | ❌ | ✅ |
| Metrics/Charts | Basic | Enhanced |
| API endpoints | 4 | 6 |
| Mobile responsive | ✅ | ✅ |

**When to use Standard**:
- Simple task list needed
- Filter and search tasks
- Lightweight, fast loading

**When to use Enhanced**:
- Multiple view perspectives needed
- Visual workflow management
- Strategic planning and roadmaps
- Deadline and calendar tracking

---

## Future Enhancements

Planned features:

- [ ] Drag-and-drop in Kanban board
- [ ] Interactive Gantt chart (zoom, pan)
- [ ] Real-time charts with Chart.js/D3.js
- [ ] Export views to PDF/PNG
- [ ] Custom dashboard layouts
- [ ] Dark mode theme
- [ ] WebSocket live updates
- [ ] Task editing from dashboard
- [ ] Burndown charts
- [ ] Team member views

---

## Development

### File Structure
```
scripts/
├── dashboard_server.py              # HTTP server (updated)
├── project_dashboard.html           # Standard dashboard
├── project_dashboard_enhanced.html  # Enhanced dashboard (NEW)
└── test_dashboard.py                # Testing script
```

### Testing
```bash
# Start server
python scripts/dashboard_server.py --port 9080

# Test standard dashboard
curl http://127.0.0.1:9080/dashboard

# Test enhanced dashboard
curl http://127.0.0.1:9080/enhanced

# Test API endpoints
curl http://127.0.0.1:9080/api/tasks
curl http://127.0.0.1:9080/api/roadmap
curl http://127.0.0.1:9080/api/sprints
```

### Extending

To add features:

1. **New API endpoint**: Edit `dashboard_server.py`, add handler method
2. **New view**: Edit `project_dashboard_enhanced.html`, add view div and JS
3. **New visualization**: Add canvas element and rendering function

---

## Support

For issues or questions:

1. Check this documentation
2. Review `doc/DASHBOARD_README.md` for standard dashboard
3. Check server logs for errors
4. Create GitHub issue with details

---

**Version**: 2.0 (Enhanced)  
**Created**: 2026-02-07  
**File**: `doc/DASHBOARD_ENHANCED_README.md`
