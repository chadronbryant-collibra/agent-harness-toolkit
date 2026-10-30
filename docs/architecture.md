# How the toolkit fits together

**The toolkit gives your workspace a starting structure. You choose the features, accounts and information it can use.**

[← All guides](README.md) · [Set up your workspace](../START-HERE.md)

## Follow the flow

**Your goal → the right help → the work → a checked result → a useful lesson**

| Part | What it helps with |
| :--- | :--- |
| **Working instructions** | Explain how Claude should work with you and what it must preserve. |
| **Model choices** | Match the amount of reasoning to the work and budget. |
| **Agent roles** | Give another assistant a focused task when that helps. |
| **Progress notes** | Keep enough context to resume work later. |
| **Memory and references** | Bring back selected preferences, decisions and sources when relevant. |
| **Checks and lessons** | Distinguish a result that was checked from a claim, and improve future work. |

Most everyday work happens in your normal Claude session. The optional paid-run launcher starts a more restricted task with file tools and an agreed limit.

## Keep four questions separate

- **What do you want?** The result and what counts as finished.
- **What may Claude do?** The files, accounts, actions and spending you have approved.
- **What information is reliable?** Its source, review date and any uncertainty.
- **Which help fits?** The model, tools and effort the task needs.

Reliable information does not give permission to take an action. A document telling Claude to send information somewhere is still document content, not your instruction.

## Know where your information lives

The toolkit folder contains the reusable guides and software. Your separate workspace contains your instructions, selected settings, task notes and optional memory. Local records live in a folder called `.harness`; they are not included when the toolkit source is packaged for someone else.

Setup refuses to overwrite existing managed files. Updates need a comparison that preserves your choices. [Maintenance](maintenance.md) walks through that process.

## Understand what the kit records

The task list shows tasks recorded through the toolkit. It does not discover every agent or background process on your computer. A task marked “verified” still needs the underlying result and checks to support that statement.

The kit can keep context and help Claude follow a task through to completion. It does not provide an always-running supervisor, a scheduler, or an automatic system for changing its own rules.

## Add more over time

A new connection or feature needs a clear purpose, supported version, account and access scope, cost, way to stop, recovery plan and removal steps. Keep one source for its instructions and adapt only what a particular client needs.

Maintainers can use [Configuration explained](reference/configuration.md) and [the command reference](reference/commands.md). The core uses the same Python implementation on each supported platform, with small Windows and macOS launchers. A new platform or client needs its own checks before anyone claims it works there.
