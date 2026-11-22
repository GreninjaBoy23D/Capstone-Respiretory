# Runbook — ROM to SoundFont Converter

For the person operating this system, possibly at an inconvenient hour, possibly without you.
Every command below has been run by a human on a machine that is not the author's laptop.

## 1. Where it runs

| Environment | Where | Who has access | How to get in |
|---|---|---|---|
| Local | developer machine | anyone with the repo | see `README.md` |
| Skeleton.cmd | developer machine | anyone with the repo | Open Skeleton.cmd to start using the tool |
| ROM Sample Extractor | import_rom.py | anyone with the repo | copy the path of our ROM file, paste it on the interface of Skeleton.cmd. |

Where the data actually lives: imported_roms (created after importing a ROM file to the tool)
Where the logs actually live: imported_roms (Audio logs are created within this folder)

## 2. Start, stop, restart

```
# start
{{command}}
# expected: {{success line}}

# stop
{{command}}

# restart after a config change
{{command}}
```

## 3. Health check

The one thing you run to answer "is it alive?":

```
{{command or curl}}
```

Healthy looks like: `{{exact output}}`
Unhealthy looks like: `{{exact output}}` → go to section 6.

## 4. Routine operations

| Task | Command | How often | Expected result |
|---|---|---|---|
| Back up the data | `{{command}}` | {{cadence}} | {{file/size}} |
| Restore from a backup | `{{command}}` | on demand | {{how you verify it worked}} |
| Apply a schema change | `{{command}}` | on release | {{output}} |
| Rotate a key or secret | {{steps}} | {{cadence}} | {{how you verify}} |
| Seed demo data | `{{command}}` | for demos | {{output}} |

## 5. Normal readings

So the operator can tell abnormal from normal:

- Startup time: about {{N}} seconds.
- Typical response time for {{the main operation}}: about {{N}} ms.
- Log lines you should expect to see and safely ignore: {{examples}}.
- Known limits: {{rate limits, row counts, concurrent users, disk}} — behavior at the limit: {{what happens}}.

## 6. Failure catalogue

Copy this block once per failure. Write these from your defect log, not from imagination.

### F-01 — {{Short symptom, in the operator's words}}

- **Symptom:** {{exact error text or observed behavior}}
- **First check:** `{{command}}` → {{what you are looking for}}
- **Likely cause:** {{cause}}
- **Fix:** `{{command or steps}}`
- **Verify the fix:** {{the health check or the specific action that should now work}}
- **If that does not work:** {{next thing to try, or "stop and escalate — see section 7"}}

### F-02 — {{...}}

## 7. Escalation and the things only a human can decide

- Data loss suspected → **stop.** Do not restart. {{who to contact, what to preserve}}.
- A third-party service is down → {{status page URL}}; the system {{degrades how}}.
- A secret may be exposed → rotate first, investigate second. Steps: {{...}}.
- Contact: {{name, email, expected response time — and, after handoff, who owns this instead}}.

## 8. Last verified

This runbook was executed end to end on {{date}} by {{name}} on {{machine/OS}}.
Anything not verified on that date is marked **UNVERIFIED** in the text above.
