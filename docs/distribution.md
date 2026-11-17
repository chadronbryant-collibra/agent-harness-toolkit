# Give someone a useful starting point

**Share the toolkit and its setup guide. Let the recipient choose their own accounts, sources, preferences and budget.**

[← All guides](README.md) · [First-time setup](../START-HERE.md)

## What to send

Send the versioned ZIP linked from the [toolkit README](../README.md), with this message:

> Unpack this folder and open START-HERE.md with Claude. Choose a folder, try the workshop example, and reopen it in a fresh session to pick up your progress.

GitHub keeps the original colleague preview as a dated snapshot. Use the 1.0 release for the current walkthrough. Check the terms included with the release before adapting or redistributing files.

## What stays yours

Do not send your workspace settings, saved memory, task notes, credentials, connection files or private source documents. The reusable kit contains generic instructions and fictional examples, not your working information.

The recipient signs in with their own approved accounts. A shared ZIP or repository link does not connect services, invite collaborators or grant access to your sources.

## Choose a version you can identify

For a handoff you may need to support later, use a named source revision or a versioned package and keep its checksum. A checksum is a short fingerprint of a file: it helps show whether the bytes changed.

The main-branch source download changes when new work is merged. The separately built package includes a list of file checksums. Send its overall checksum through a trusted route if the recipient needs to verify who supplied it; a checksum inside an archive alone cannot prove authenticity.

## For the person building the handoff

Build from reviewed, committed source. The package builder includes only the selected toolkit files and omits Git history, local workspace data, credentials and caches. Verify the archive and try the setup from a clean extraction before sharing it.

[Package commands](reference/commands.md#check-and-package-the-toolkit) · [Setup checks](acceptance.md)
