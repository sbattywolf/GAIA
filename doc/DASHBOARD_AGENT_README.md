# GAIA Agent Dashboard

## Overview

The Agent Dashboard provides individual monitoring and metrics for each agent in the GAIA system. This dashboard allows you to:

- Monitor agent performance and status
- View agent-specific metrics and statistics
- Track agent activities and recent actions
- Review agent configuration details

## Features

### 1. Agent Selection
- Tab-based interface for switching between agents
- Visual status indicators (active/inactive)
- Quick navigation between different agents

### 2. Agent Overview
- Agent ID, version, and model information
- Description and configuration details
- Status indicator with real-time updates

### 3. Performance Metrics
- **Tasks Processed**: Total number of tasks handled by the agent
- **Success Rate**: Percentage of successfully completed tasks
- **Average Response Time**: Mean time to process requests (in seconds)
- **Uptime**: Total hours the agent has been running
- **Errors**: Count of errors encountered
- **Warnings**: Count of warnings generated

### 4. Recent Activity
- Real-time activity log showing recent agent actions
- Timestamps for each activity
- Clear description of actions performed

### 5. Configuration Details
- Complete agent configuration in table format
- All properties and values displayed
- Easy reference for troubleshooting

## Quick Start

### Start the Dashboard Server

```bash
# From project root
cd /home/runner/work/GAIA/GAIA

# Start the server
python scripts/dashboard_server.py --port 9080
```

### Access the Agent Dashboard

Open your browser and navigate to:
- **Agent Dashboard**: http://127.0.0.1:9080/agents

### Navigation

1. The dashboard will load all configured agents from `agents.json`
2. Click on any agent tab to view its details
3. The dashboard auto-refreshes every 30 seconds
4. Switch between agents at any time using the tabs

## API Endpoints

The Agent Dashboard uses the following API endpoints:

### Get All Agents
```
GET /api/agents
```

**Response Example:**
```json
[
  {
    "id": "alby-online-0.3",
    "name": "Alby Online",
    "version": "0.3",
    "module": "agents.alby_online_agent",
    "status": "active",
    "description": "Alby online agent (service mode)",
    "model": "gpt-4o-mini"
  }
]
```

### Get Agent Metrics
```
GET /api/agent/{agent_id}/metrics
```

**Response Example:**
```json
{
  "agent_id": "alby-online-0.3",
  "tasks_processed": 127,
  "success_rate": 94.5,
  "avg_response_time": 1.23,
  "uptime_hours": 168,
  "last_active": "2026-02-07T03:30:00Z",
  "errors": 2,
  "warnings": 8,
  "recent_activities": [
    {
      "time": "2 minutes ago",
      "action": "Processed task T042"
    },
    {
      "time": "15 minutes ago",
      "action": "Created GitHub issue #123"
    }
  ]
}
```

## Metrics Explanation

### Tasks Processed
Total number of tasks the agent has handled since startup or last reset. This includes both successful and failed tasks.

### Success Rate
Percentage of tasks completed successfully without errors. Calculated as:
```
Success Rate = (Successful Tasks / Total Tasks) * 100
```

**Thresholds:**
- ✅ **Green (Success)**: ≥ 95%
- ⚠️ **Yellow (Warning)**: 80-94%
- ❌ **Red (Danger)**: < 80%

### Average Response Time
Mean time taken to process a single task, measured in seconds. Lower is better.

**Typical ranges:**
- Fast: < 1 second
- Normal: 1-3 seconds
- Slow: > 3 seconds

### Uptime
Total hours the agent has been running continuously. Resets when agent restarts.

### Errors
Count of critical errors that prevented task completion.

### Warnings
Count of non-critical issues that occurred during processing.

## Use Cases

### 1. Monitor Agent Health
**Goal**: Check if agents are running properly

**Steps:**
1. Open Agent Dashboard
2. Check status indicators (green = active)
3. Review success rate (should be > 90%)
4. Check error count (should be low)

### 2. Debug Agent Issues
**Goal**: Investigate why an agent is failing

**Steps:**
1. Select the problematic agent
2. Check recent activity log for error messages
3. Review success rate trend
4. Check configuration for misconfigurations

### 3. Performance Optimization
**Goal**: Identify slow or overloaded agents

**Steps:**
1. Compare response times across agents
2. Identify agents with high task counts
3. Check for agents with many warnings
4. Plan resource allocation accordingly

### 4. Capacity Planning
**Goal**: Understand agent workload distribution

**Steps:**
1. Review tasks processed by each agent
2. Identify underutilized agents
3. Check uptime to ensure availability
4. Plan for scaling or rebalancing

## Troubleshooting

### Dashboard Shows "No agents configured"
**Cause**: The `agents.json` file is empty or missing.

**Solution:**
```bash
# Check if agents.json exists
ls -la agents.json

# View contents
cat agents.json

# Ensure it contains valid JSON array
```

### Agent Metrics Show Zero
**Cause**: Agent hasn't processed any tasks yet or metrics not being collected.

**Solution:**
1. Verify agent is running
2. Check if tasks are being assigned to the agent
3. Review agent logs for errors

### Dashboard Not Loading
**Cause**: Server not running or wrong port.

**Solution:**
```bash
# Check if server is running
ps aux | grep dashboard_server

# Start server if not running
python scripts/dashboard_server.py --port 9080

# Check network connectivity
curl http://127.0.0.1:9080/api/agents
```

### Status Indicators Always Show Inactive
**Cause**: Agent status not being updated in `agents.json`.

**Solution:**
Agents need to update their status. This can be implemented by having agents write their status to a shared location that the dashboard reads.

## Customization

### Add Custom Metrics
To add custom metrics for an agent:

1. Update the agent to write metrics to a metrics store
2. Modify `/api/agent/{agent_id}/metrics` endpoint to read these metrics
3. Update the dashboard HTML to display new metrics

### Change Refresh Rate
The dashboard auto-refreshes every 30 seconds. To change this:

```javascript
// In agent_dashboard.html, find:
setInterval(async () => {
    // ...
}, 30000);  // Change this value (in milliseconds)
```

### Style Customization
All styles are embedded in the HTML. Modify the `<style>` section in `scripts/agent_dashboard.html`:

```css
/* Example: Change primary color */
.stat-card .value {
    color: #your-color-here;
}
```

## Integration with Other Dashboards

The Agent Dashboard complements the other dashboards:

| Dashboard | Purpose | Link |
|-----------|---------|------|
| **Standard Dashboard** | Project overview, tasks, timeline | `/dashboard` |
| **Enhanced Dashboard** | Multi-view (Kanban, Roadmap, Calendar) | `/enhanced` |
| **Agent Dashboard** | Individual agent monitoring | `/agents` |

### Typical Workflow

1. Start with **Standard Dashboard** for project overview
2. Use **Enhanced Dashboard** for detailed task management
3. Check **Agent Dashboard** to monitor execution health
4. Return to appropriate dashboard based on needs

## Advanced Features

### Per-Agent Activity Filtering
Filter activities by type or time range (future enhancement):

```javascript
// Example implementation
function filterActivities(agentId, filters) {
    const activities = agentMetrics.recent_activities;
    return activities.filter(a => {
        // Apply filters
        return true;
    });
}
```

### Export Agent Metrics
Export metrics to CSV or JSON for analysis:

```javascript
// Add export button
function exportMetrics(agentId) {
    const data = JSON.stringify(agentMetrics, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `agent-${agentId}-metrics.json`;
    a.click();
}
```

### Real-Time Updates via WebSocket
For live updates without polling (future enhancement):

```javascript
// WebSocket connection
const ws = new WebSocket('ws://localhost:9080/ws/agent/' + agentId);
ws.onmessage = (event) => {
    const metrics = JSON.parse(event.data);
    updateDashboard(metrics);
};
```

## Best Practices

### 1. Regular Monitoring
- Check agent dashboards at least once per day
- Set up alerts for error thresholds
- Review trends over time

### 2. Performance Baselines
- Establish baseline metrics for each agent
- Compare current metrics to baseline
- Investigate significant deviations

### 3. Proactive Maintenance
- Restart agents with declining success rates
- Address warnings before they become errors
- Keep agents updated to latest versions

### 4. Documentation
- Document agent-specific configurations
- Keep notes on typical metrics ranges
- Record troubleshooting steps

## Future Enhancements

Planned improvements:

- [ ] Historical metrics charts (time series)
- [ ] Alert thresholds configuration
- [ ] Agent comparison view
- [ ] Metrics export functionality
- [ ] Real-time WebSocket updates
- [ ] Custom dashboard layouts
- [ ] Agent health scores
- [ ] Automated recommendations

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review agent logs in `.tmp/` directory
3. Verify API endpoints are responding
4. Check browser console for JavaScript errors

## See Also

- [Dashboard Enhanced README](./DASHBOARD_ENHANCED_README.md) - Multi-view dashboard
- [Dashboard README](./DASHBOARD_README.md) - Standard dashboard
- [Agent Session Recovery](./agent_session_recovery.md) - Agent recovery procedures
