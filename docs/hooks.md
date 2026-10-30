# Add helpful reminders

**Hooks can remind Claude how you want work to start, continue and finish.** They are optional. Get a normal task working before adding them.

[← All guides](README.md) · [Maintenance](maintenance.md)

## What the included reminders do

| Moment | Reminder |
| :--- | :--- |
| **A session starts** | Read your instructions, confirm the task and limits, and find only the context that matters. |
| **Claude shortens a long conversation** | Preserve the goal, decisions, work completed and next checks in a short progress note. |
| **Claude finishes a response** | Explain the result, what was checked and anything still unresolved. |

The technical names for these moments are `SessionStart`, `PreCompact` and `Stop`. You do not need to memorize them.

These reminders do not save progress on their own, guarantee Claude follows every instruction, or enforce access restrictions. They do not make additional model calls. The toolkit's restricted paid-run launcher disables custom reminders and other customizations for that run.

## Ask Claude to help you decide

> Review how I use this workspace. Would the included reminders help? If so, check that my Claude version supports them, show me the settings change, and preserve anything already configured.

Claude should preview the change before applying it. It should then open a fresh session and check that the selected reminder actually runs. Creating a settings entry is only part of setup.

## Keep your existing settings

The toolkit saves a copy of the previous settings and adds its reminders at project level. Keep that copy private; existing settings may contain information specific to your organization.

Keep the toolkit folder in its chosen location. Moving it can break the paths used by reminders.

## Turn them off

> Remove the toolkit's reminders and preserve my other settings. If anything changed since they were added, show me the differences before restoring the old version.

Automatic removal works only while the settings still match what the toolkit wrote. If they have changed, Claude needs to remove the selected entries without discarding your later edits.

If a reminder fails, it is intended to let ordinary work continue. It is a prompt to help the assistant, not a security control.

[Commands for Claude](reference/commands.md#add-or-remove-reminders) · [Official hook reference](https://code.claude.com/docs/en/hooks)
