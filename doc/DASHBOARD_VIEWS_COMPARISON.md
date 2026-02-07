# GAIA Dashboard Views - Quick Reference

## Overview of Available Views

GAIA provides two dashboard options with different views optimized for various workflows.

## Standard Dashboard
**URL**: `http://127.0.0.1:9080/dashboard`

### Views (4)
1. **📊 Overview** - Key metrics and progress
2. **📋 Tasks** - Filterable task table
3. **🤖 Agents** - Agent status and configuration
4. **📈 Timeline** - Basic timeline view

### Best For
- Quick task lookups
- Searching and filtering tasks
- Simple status overview
- Lightweight, fast loading

---

## Enhanced Dashboard (NEW!)
**URL**: `http://127.0.0.1:9080/enhanced`

### Views (6)

#### 1. 📊 Overview
**Purpose**: High-level project health

**Shows**:
- Total tasks
- Completed tasks (%)
- In-progress count
- Critical priority count
- Hours completed / total
- Priority breakdown
- Status breakdown

**Use When**:
- Starting your day
- Daily standups
- Stakeholder updates
- Quick health check

---

#### 2. 📋 Kanban Board
**Purpose**: Visual workflow management

**Shows**:
- Three columns: Pending → In Progress → Completed
- Task cards with priorities
- Estimated hours
- Task counts per column

**Use When**:
- Sprint planning
- Moving tasks through workflow
- Team collaboration
- Visual task organization

---

#### 3. 🗺️ Roadmap
**Purpose**: Strategic planning and sprints

**Shows**:
- Tasks grouped by sprint/milestone
- Timeline of sprints
- Task status per sprint
- Priority indicators

**Use When**:
- Sprint planning
- Release planning
- Long-term roadmap review
- Milestone tracking

**Data Required**:
- `sprint` or `milestone` field on tasks

---

#### 4. 📈 Gantt Timeline
**Purpose**: Visual progress tracking

**Shows**:
- Horizontal progress bars
- Task completion percentage
- Up to 20 recent/active tasks
- Visual timeline

**Use When**:
- Progress reviews
- Deadline tracking
- Identifying blocked tasks
- Team velocity tracking

---

#### 5. 📅 Calendar
**Purpose**: Deadline and event tracking

**Shows**:
- Monthly calendar grid
- Tasks on deadline dates
- Month navigation
- Overflow indicators

**Use When**:
- Planning deadlines
- Scheduling work
- Avoiding date conflicts
- Sprint planning

**Data Required**:
- `deadline` or `target_date` field on tasks

---

#### 6. 📊 Metrics
**Purpose**: Analytics and insights

**Shows**:
- Task completion trends
- Priority distribution
- Hours by status
- Velocity tracking

**Use When**:
- Sprint retrospectives
- Performance analysis
- Identifying bottlenecks
- Data-driven decisions

---

## Quick Comparison

| Feature | Standard | Enhanced |
|---------|----------|----------|
| Views | 4 | 6 |
| Kanban Board | ❌ | ✅ |
| Roadmap | ❌ | ✅ |
| Calendar | ❌ | ✅ |
| Gantt Timeline | Basic | Enhanced |
| Metrics/Charts | Basic | Enhanced |
| Task Filtering | ✅ | Limited |
| Load Time | Faster | Normal |

---

## View Selection Guide

### By Use Case

| Use Case | Recommended View |
|----------|-----------------|
| Daily standup | Enhanced → Overview |
| Sprint planning | Enhanced → Kanban + Roadmap |
| Progress review | Enhanced → Gantt Timeline |
| Deadline planning | Enhanced → Calendar |
| Retrospective | Enhanced → Metrics |
| Quick lookup | Standard → Tasks |
| Filter/search | Standard → Tasks |

### By Role

| Role | Primary View | Secondary View |
|------|-------------|----------------|
| Developer | Kanban Board | Timeline |
| Project Manager | Roadmap | Overview |
| Team Lead | Overview | Metrics |
| Product Owner | Roadmap | Calendar |
| Scrum Master | Kanban | Metrics |

---

## Workflow Examples

### Morning Routine
1. Open **Enhanced → Overview** - Check overnight progress
2. Switch to **Kanban** - Review your tasks
3. Check **Calendar** - Note today's deadlines

### Sprint Planning Meeting
1. **Roadmap** - Review current sprint status
2. **Kanban** - Pull tasks from backlog to "Pending"
3. **Calendar** - Mark sprint end date
4. **Gantt Timeline** - Verify no conflicts

### End of Sprint
1. **Metrics** - Analyze completion rate
2. **Overview** - Calculate velocity
3. **Roadmap** - Plan next sprint
4. **Kanban** - Archive completed tasks

---

## Data Requirements

### Minimal (Works with all views)
```json
{
  "id": "T001",
  "title": "Task title",
  "status": "pending",
  "priority": "high"
}
```

### Recommended (Enables most features)
```json
{
  "id": "T001",
  "title": "Task title",
  "status": "in-progress",
  "priority": "high",
  "est_hours": 8,
  "progress": 50
}
```

### Complete (All features enabled)
```json
{
  "id": "T001",
  "title": "Implement user auth",
  "description": "Add OAuth2 flow",
  "status": "in-progress",
  "priority": "high",
  "est_hours": 8,
  "progress": 60,
  "sprint": "Sprint 2",
  "milestone": "Q1 2026 - MVP",
  "deadline": "2026-02-20T17:00:00Z",
  "added_at": "2026-02-01T09:00:00Z",
  "last_updated": "2026-02-07T14:30:00Z"
}
```

---

## Enrich Your Data

To enable all enhanced dashboard features:

```bash
# Preview enrichment
python scripts/enrich_sample_data.py --preview

# Apply enrichment (creates backup)
python scripts/enrich_sample_data.py

# View sample enriched task
python scripts/enrich_sample_data.py --sample
```

This adds:
- Sprint assignments
- Milestones (for high priority)
- Deadlines (spread over 60 days)
- Progress percentages

---

## Access URLs

### Standard Dashboard
```
http://127.0.0.1:9080/dashboard
```

### Enhanced Dashboard
```
http://127.0.0.1:9080/enhanced
```

### Launch Commands
```bash
# Standard
python scripts/dashboard_server.py

# Enhanced (auto-opens browser)
python scripts/launch_enhanced_dashboard.py

# Enhanced on custom port
python scripts/launch_enhanced_dashboard.py --port 8080
```

---

## Performance Notes

### Standard Dashboard
- **Load Time**: < 1 second
- **Best For**: < 100 tasks
- **Memory**: Low
- **Refresh**: 30 seconds

### Enhanced Dashboard
- **Load Time**: 1-2 seconds
- **Best For**: < 200 tasks
- **Memory**: Medium
- **Refresh**: 30 seconds

### Optimization Tips
- Use filters to reduce visible tasks
- Archive completed tasks periodically
- Consider pagination for 100+ tasks
- Use standard dashboard for quick lookups

---

## Keyboard Shortcuts

*Coming Soon*

- `1-6`: Switch between views
- `r`: Refresh data
- `f`: Focus search/filter
- `esc`: Clear filters

---

## Troubleshooting

### Views Not Loading
**Check**: Server is running
```bash
curl http://127.0.0.1:9080/api/stats
```

### Roadmap Empty
**Cause**: Tasks missing `sprint` field
**Fix**: Run enrichment script
```bash
python scripts/enrich_sample_data.py
```

### Calendar Empty
**Cause**: Tasks missing `deadline` field
**Fix**: Run enrichment script

### Kanban Shows All in One Column
**Cause**: Tasks all have same status
**Fix**: Update task statuses to "pending", "in-progress", or "completed"

---

## Further Reading

- [Dashboard Enhanced README](DASHBOARD_ENHANCED_README.md) - Complete documentation
- [Dashboard README](DASHBOARD_README.md) - Standard dashboard docs
- [API Documentation](DASHBOARD_ENHANCED_README.md#api-endpoints) - API reference

---

**Quick Decision**: 
- Need to find a specific task? → **Standard Dashboard**
- Need to see the big picture? → **Enhanced Dashboard**

**Created**: 2026-02-07  
**Version**: 2.0
