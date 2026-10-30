# Give someone a useful starting point

**Share the toolkit and its setup guide. Let the recipient choose their own accounts, sources, preferences and budget.**

[← All guides](README.md) · [First-time setup](../START-HERE.md)

## What to send

Send the current toolkit ZIP, or a link to the current source download, with this message:

> Unpack this folder and open START-HERE.md with Claude. It will help you choose what you need, check your computer, and walk you through a first task. You do not need to understand every file before starting.

The GitHub repository is publicly viewable. Its older preview release remains a dated snapshot; the main-branch download includes the refreshed guides. Public visibility does not establish an open-source license or permission to redistribute third-party material. Confirm the applicable ownership and distribution terms before broader reuse.

## What stays yours

Do not send your workspace settings, saved memory, task notes, credentials, connection files or private source documents. The reusable kit contains generic instructions and fictional examples, not your working information.

The recipient signs in with their own approved accounts. A shared ZIP or repository link does not connect services, invite collaborators or grant access to your sources.

## Choose a version you can identify

For a handoff you may need to support later, use a named source revision or a versioned package and keep its checksum. A checksum is a short fingerprint of a file: it helps show whether the bytes changed.

The main-branch source download changes when new work is merged. The separately built package includes a list of file checksums. Send its overall checksum through a trusted route if the recipient needs to verify who supplied it; a checksum inside an archive alone cannot prove authenticity.

## For the person building the handoff

Build from reviewed, committed source. The package builder includes only the selected toolkit files and omits Git history, local workspace data, credentials and caches. Verify the archive and try the setup from a clean extraction before sharing it.

[Package commands](reference/commands.md#check-and-package-the-toolkit) · [Setup checks](acceptance.md)
