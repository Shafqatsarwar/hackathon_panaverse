# Chat History

This folder contains daily logs of all assistant activities.

## Structure

Each day creates a new JSON file: `YYYY-MM-DD.json`

## Log Format

```json
[
  {
    "timestamp": "2026-01-23T00:05:00",
    "task": "email_check",
    "data": {
      "status": "completed",
      "emails_found": 2,
      "emails": [
        {
          "subject": "PIAIC Quiz Tomorrow",
          "priority": "high"
        }
      ]
    }
  }
]
```

## Usage

View today's activity:
```bash
cat chat_history/2026-01-23.json
```

View all history:
```bash
ls chat_history/
```

## Privacy

- Chat history is local only
- Not synced to cloud
- Can be deleted anytime
