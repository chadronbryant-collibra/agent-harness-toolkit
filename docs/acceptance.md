# Check that your setup works

**Finish setup by completing something useful and checking the result.** A file in the right folder is a start; seeing the selected feature work is the next step.

[← All guides](README.md) · [First-time setup](../START-HERE.md)

## Ask Claude to walk through the checks

> Help me check the features we enabled. Use harmless examples, show what actually worked, and list anything we have not tried. Do not start a paid task or connect a service unless we agreed to it.

| Check | What you should be able to see |
| :--- | :--- |
| **Instructions** | A fresh Claude session can find and follow the working instructions. |
| **First task** | The fictional example produces an action plan with sources and clear open questions. |
| **Continuity** | A saved progress note lets you pick up an interrupted task. |
| **Agents, if selected** | The intended role appears and completes a clearly defined example. |
| **Memory, if enabled** | A harmless note can be saved, found, corrected and removed. |
| **Reminders, if enabled** | The selected reminder actually runs in a fresh session. |
| **Spending** | You understand your limits, what the records cover and what is still unknown. |
| **Recovery** | Claude can explain how to undo a change or uninstall while keeping your work. |

You can leave optional features off. Record them as “not enabled” rather than treating them as broken or pretending they were tested.

## Leave a short setup note

Ask Claude to record the choices you made, relevant versions, the examples you tried, what worked, and what remains. Keep source contents, passwords and chat transcripts out of that note.

A useful result sounds like: “The instructions loaded and the example task worked. Memory is off. Reminders have not been tried yet.”

## For people maintaining the toolkit

Before claiming support for a platform or client, check that actual surface. Automated tests of the local software do not establish account access, a working Claude connection or a person's ability to complete the walkthrough.

Include positive and failure cases for setup, files with spaces in their paths, budgets, changed settings, memory, interruptions and package integrity. Test subprocess cancellation and supported filesystem protections on the real OS. Keep x64 and arm64 results separate when a claim depends on architecture. Package checks should include the file list, checksums, extraction and a basic run from the extracted copy.

No paid model call is needed for the local test suite. A live Claude or billing check requires the correct account and the spending permission for that example.

[Recorded checks](validation-2026-10-30.md) · [Maintainer commands](reference/commands.md#check-and-package-the-toolkit)
