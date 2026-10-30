# Setup playbook for Claude

**Use this page to guide the setup. Keep the person's experience conversational.** Explain decisions and results in plain language; run necessary checks yourself when the session has permission and the tools to do so.

[← First-time setup](../../START-HERE.md) · [Command reference](commands.md) · [Configuration explained](configuration.md)

## 1. Understand the person and the computer

Read the toolkit README, [How the toolkit works](../architecture.md), and [Information and permissions](../security.md). Ask what work the person wants help with, approved storage, relevant organization rules, their billing arrangement and budget. Ask only for information you cannot establish from the current session.

Run the local diagnostic from the toolkit folder. It reports the OS, architecture, Python version and whether selected tools can be found. Python 3.11 or later is required. On Windows, `py -3` may be the available command; on macOS it may be `python3`.

Distinguish native Windows from WSL and a local Claude session from a chat that cannot open files. Do not treat a visible executable as proof of sign-in or account access. Inspect selected metadata only, never whole environments, credentials or complete configuration files for display.

## 2. Recommend a small starting setup

Start with working instructions, sensible model choices and one familiar task. Memory, reminders, agents and outside connections are choices, not prerequisites.

Explain what the kit supplies and what remains to be configured. The sample $1 task and $20 monthly limits are examples, not spending authority. Do not start paid tasks, add connections, schedule work or capture memory without the selected scope and permission.

## 3. Preview the files

Choose an existing empty workspace folder separate from the toolkit source. Run the setup preview and explain its filenames. It creates working instructions, selected settings and three agent-role files when applied.

After the person accepts the concrete plan, use the exact `plan_sha256` returned by the preview. If the plan changes or files already exist, stop that apply attempt. Read existing instructions and preserve the person's edits in any agreed manual merge. Do not overwrite or choose a substitute file just to bypass refusal.

## 4. Configure the selected choices

Use [Configuration explained](configuration.md). Confirm the actual billing mode, approved dollar limits and available models before recording them as checked. A `verified` flag records a review; it does not authenticate an account or establish permission.

For subscription work, keep the normal interactive route and provider account controls. The paid-run launcher requires an explicitly metered profile. Explain what its spending record covers and what it does not.

Agent templates start with suggested model families. Adjust their model choices only to the person's selected, supported models. Open a fresh session to check discovery. Installing a file is not proof it loaded or ran.

## 5. Add only selected optional features

**Memory:** agree what may be stored, where and for how long before enabling it. Explain that the included store is plaintext. Test with a harmless note: save, find, correct and remove it. Do not import another person's store or transcripts. Sensitive sources need a separately approved storage feature.

**Reminders:** check current client support for command hooks with explicit `args`. Preview the settings merge, apply the exact returned binding after agreement, and verify actual events in a fresh session. Preserve existing handlers. Keep the toolkit's absolute location stable.

**Tools and connections:** use [Extend your setup](../extensions.md). Check official guidance, account, organization, destination, access and cost for the selected operation. No bulk installation, credential discovery or account borrowing. GitHub is optional. Install the included harness skill only in a supported location, checking for an existing copy first.

## 6. Finish with a useful task

Copy the included fictional notes into the chosen workspace without overwriting existing files. Complete the action-plan exercise, then walk through the selected items in [Check your setup](../acceptance.md).

Leave a short setup note with the toolkit and workspace locations, choices, versions, checks actually completed and remaining work. Distinguish a source file, an installed file, a loaded feature, a successful invocation and the person's acceptance. Keep source contents, credentials and transcripts out of operational records.

Explain how to start the next task, resume after a pause, review spending and find maintenance help. If a required step is unavailable, finish independent steps and name the exact remaining action.
