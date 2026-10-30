# Command reference for Claude and maintainers

**You can skip this page during ordinary use.** Ask Claude to use the relevant commands and explain the result. These examples are instructions, not records of commands that already ran.

[← All guides](../README.md) · [Setup playbook](setup-for-claude.md) · [Configuration](configuration.md)

Run commands from the toolkit folder. `python` below means the available Python 3.11+ interpreter; Claude should select `python3` or `py -3` when appropriate. Replace placeholders such as `<workspace>` with actual values. Quote paths that contain spaces. Do not paste the angle-bracket placeholders literally.

## Inspect and set up a workspace

```text
python toolkit.py doctor
python toolkit.py self-check
python toolkit.py --workspace "<workspace>" init
```

`doctor` reports local prerequisites without signing in or making a model call. Windows architecture may be reported from environment metadata, rather than independently verified. `self-check` runs a small fictional routing example; it does not prove the client is installed or signed in.

`init` previews the files and returns `plan_sha256`. Review the plan before applying it:

```text
python toolkit.py --workspace "<workspace>" init --apply-plan <plan_sha256>
```

Apply refuses existing managed files or a changed plan. It writes an installation record so unchanged toolkit-owned files can later be identified. A result of `configured-not-loaded` means a fresh client check is still needed.

## Choose and preview a task

Create a task description using [the example](../../examples/task.json), with the user's actual outcome, allowed action and completion checks. Keep source text separate from permission to act.

```text
python toolkit.py --workspace "<workspace>" assess --task "<task-file.json>"
python toolkit.py --workspace "<workspace>" route --task "<task-file.json>"
python toolkit.py --workspace "<workspace>" task --input "<task-file.json>"
```

`assess` separates the stated intent, allowed action, declared source quality and model choice. Source ranks depend on metadata supplied by the caller; they do not authenticate it. `route` recommends a role without starting a call. `task` saves a progress record and returns its ID.

For the optional metered launcher, first verify the account and model, agree the spending limit and confirm the task is in the permitted state:

```text
python toolkit.py --workspace "<workspace>" run --id <task-id> --usd 0.50
```

This is a preview. Adding `--execute` starts the paid provider call and requires spending permission. The launcher permits file tools only. It checks supported client flags, reserves the allowance, limits time/output, and leaves acceptance of the artifact for a later check.

The launcher records the task as `working`. A returned process result does not mark it verified or delivered. Never restart an uncertain run merely because a result did not appear.

## Understand budget records

```text
python toolkit.py --workspace "<workspace>" budget-status
python toolkit.py --workspace "<workspace>" reserve --usd 0.50
python toolkit.py --workspace "<workspace>" reconcile --id <reservation-id> --actual-usd 0.12
```

Manual `reserve` and `reconcile` are for inspecting or maintaining accounting. Do not manually reserve the same allowance before `run`; the launcher reserves its own amount.

A final amount needs evidence. If the amount is unavailable, reconcile without `--actual-usd`; the original allowance stays counted and actual cost remains unknown. Use `--not-started` only when there is evidence that no provider call began. It releases the reservation. Reconciliation is allowed once and keeps the original budget month. Actual overspend is recorded rather than hidden.

## Save task progress

```text
python toolkit.py --workspace "<workspace>" checkpoint --id <task-id> --status working --evidence "<short progress note or evidence pointer>"
python toolkit.py --workspace "<workspace>" agents
```

Allowed progress is `planned` → `working` or `blocked`; `working` → `working`, `blocked` or `verified`; `blocked` → `working`; and `verified` → `delivered`. Each return to `working` counts against the configured cycle limit. A verification label is a caller's statement; inspect its supporting result.

The `agents` command lists recorded tasks and their statuses. It does not inspect all processes or prove which agents are alive. Keep progress notes small and avoid source bodies, credentials or sensitive details.

## Try memory with a harmless example

After the storage/retention choice is approved and memory is enabled:

```text
python toolkit.py --workspace "<workspace>" memory remember --text "Fictional preference: use short examples" --source "user:setup-example"
python toolkit.py --workspace "<workspace>" memory search --text "short examples"
python toolkit.py --workspace "<workspace>" memory forget --id <returned-memory-id>
```

The basic store saves text, source and creation date. Searches are bounded literal text matches, not meaning-based search. Corrections require removing the old item and saving a replacement. Forget is logical deletion; it is not secure erasure of storage or backups.

## Add or remove reminders

After checking installed-client support for hooks with explicit arguments:

```text
python toolkit.py --workspace "<workspace>" hooks preview
python toolkit.py --workspace "<workspace>" hooks apply --binding <preview-binding>
python toolkit.py --workspace "<workspace>" hooks remove
```

The binding identifies the reviewed settings change. Apply preserves other settings and saves the previous bytes privately. Remove restores those bytes only if the installed settings have not changed since. Later edits need a selective manual merge, not replacement.

An interrupted apply may leave a record marked `prepared-not-confirmed`; inspect the actual settings before retrying. A synthetic `hook` payload test checks source behavior only. Verify actual session events separately.

## Check reference dates

```text
python toolkit.py references --catalog references/catalog.json
```

This compares dates in the catalog. It makes no network request, refreshes no source and proves no account permission.

## Inspect an interrupted run

These are the records to inspect, not instructions to delete them:

| Record in the workspace | What it helps establish |
| :--- | :--- |
| `.harness/active-run/owner.json` | The recorded task, reservation and process ID for an attempted launch. |
| `.harness/operation.lock` | Another toolkit operation may be changing state, or an interruption left the lock behind. |
| `.harness/tasks/` | The selected task's latest recorded progress. |
| `.harness/runs/` | Recorded process results and whether artifact acceptance is still pending. |
| `.harness/budget.json` | Reserved and known costs. |

Check the exact process and start time, current files, possible effects and budget before resolving a stale record. Process IDs can be reused. A failed process query or missing output does not prove termination. Do not auto-steal a lock, remove an uncertain run marker or repeat an uncertain write.

## Check and package the toolkit

```text
python -m unittest discover -s tests -v
python toolkit.py self-check
python scripts/package.py --output "<new-archive-outside-the-repository.zip>"
python scripts/package.py --verify "<archive.zip>"
```

Build from reviewed committed source. The builder refuses an existing output or an output inside the source folder. It includes selected files and checksums, not local workspace records. Compare an overall archive checksum through a trusted route when authenticity matters.

## Remove an installed setup

Remove optional reminders first, preserving later settings edits. Then:

```text
python toolkit.py --workspace "<workspace>" uninstall
```

Uninstall removes only unchanged files in its installation record. It retains changed files, memory, task records and budgets. Removing retained information or backups is a separate decision. Do not use `init` to update or repair an existing installation.
