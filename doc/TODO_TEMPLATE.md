# TODO List Template — Working the Todo List (step 1)

Use this template when creating or resetting a story `.current` todo list. It follows the runbook guidance (Working the Todo List — step 1).

Fields recommended per task:
- `id`: short id (t1, t2 ...)
- `title`: concise title
- `description`: short description and link to related files
- `status`: `todo` | `in-progress` | `completed`
- `priority`: `high` | `medium` | `low`
- `classification`: list (e.g., `test`, `documentation`, `governance`)
- `acceptance`: single-line acceptance criteria

Template JSON skeleton (copy and edit):

```
{
  "story": "<Story Title>",
  "story_key": "<story_key>",
  "agent": "<agent>",
  "todolist": "<todolist name>",
  "type": "current",
  "created_at": "<ISO timestamp>",
  "tasks": [
    {
      "id": "t1",
      "title": "Example task",
      "description": "Short description",
      "status": "todo",
      "priority": "high",
      "classification": ["story","documentation"],
      "acceptance": "Add tests and update runbook"
    }
  ]
}
```

Follow the naming convention for files under `.tmp/todolists/`:
`<story_key>.TD-<story_key>.<agent>.TD-<todolist>.current`
