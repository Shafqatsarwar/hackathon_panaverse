---
name: whatsapp_skill
description: Skill for sending and receiving WhatsApp messages
---

# WhatsApp Skill

This skill handles interaction with WhatsApp, allowing agents to send notifications and potentially receive commands.

## Capabilities

- Send text messages to specified numbers
- Verify delivery status (mock/simulated for now)

## Usage

```python
from skills.whatsapp_skill.skill import WhatsAppSkill

skill = WhatsAppSkill()
skill.send_message("+923001234567", "Hello from Panaversity!")
```

## Advanced Usage (Filtering)

```python
# Check for messages about PIAIC or Batch 47
messages = skill.check_messages(keywords=["PIAIC", "Panaversity", "Batch 47"])
for msg in messages:
    print(f"Found: {msg['title']} -> {msg['last_message']}")
```

## Configuration

Requires `WHATSAPP_ENABLED=true` in `.env`.
Authentication is handled via persistent browser session (QR code scan once).
