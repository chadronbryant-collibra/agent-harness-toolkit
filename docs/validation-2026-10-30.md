# What was checked on October 30, 2026

**This is the maintainer's record of checks, not a setup step.** For your own walkthrough, use [Check your setup](acceptance.md).

[← All guides](README.md)

## Local software checks

On macOS arm64 with Python 3.14.6, 42 automated tests passed. They covered setup, preserving changed files, allowed paths, budgets, local memory, reminders, task progress and package integrity. Resource warnings were treated as errors.

Selected checks used real local processes: two competing budget requests admitted only one reservation; a fictional process reported cost; a sleeping process was stopped at the time limit. Invalid output was not treated as a successful task or a cost of zero.

The shell launcher, basic diagnostic, deterministic package bytes, archive verification and a run from an extracted package were checked. The installed Claude 2.1.303 help listed the launcher options the toolkit requires. Reading that help did not start a model task.

## Later checks in GitHub

The [initial toolkit PR](https://github.com/chadronbryant-collibra/agent-harness-toolkit/pull/1) and [README update](https://github.com/chadronbryant-collibra/agent-harness-toolkit/pull/2) each had 12 passing push/PR checks across Windows, macOS and Linux with Python 3.11 and 3.13. The initial Windows Python 3.11 run exposed a diagnostic that invoked a local shell; it was corrected before merge.

The initial 35 published source files were downloaded and compared with the reviewed local files. They matched. The README update was also read back and matched its reviewed source.

## What these checks do not establish

They do not prove a fresh Claude session loads every selected instruction, agent or reminder, that a paid call works for a particular account, or that a colleague can complete the walkthrough unaided. Those need separate, attended checks.

The PowerShell launcher and every architecture/client combination have not all had an attended walkthrough. The memory store remains readable local text without its own encryption. No live paid model call or account verification was performed as part of the recorded local software checks.

These are dated observations. A later change needs the checks appropriate to that change.
