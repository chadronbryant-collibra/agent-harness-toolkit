# Local Memory Harness commands

Use this reference for exact commands, migration, and recovery. For everyday setup, start in [the short guide](../learn/context.md).

## Set up and use memory

Run these commands from the extracted toolkit, using the actual folder and the reviewed digest. Create the target folder first if it is new.

```text
python3 kit.py --workspace "/path/to/work" add memory-harness
python3 kit.py --workspace "/path/to/work" add memory-harness --apply-plan PLAN_SHA256
```

The preset installs the workspace-memory skill, a project rule to use memory when relevant, the local scripts and settings, and an ignore rule under `.harness/`. It doesn't create a database until a memory operation needs one. It preserves existing files. The same preview updates untouched helper files from earlier 1.2 releases, removes the retired helper if unchanged, and keeps the existing store. Run rebuild if you want to clear older derived search tables. Review any file conflict before applying a change. Use the separate `context` and `references` presets if you want starter files for either. Review the exact paths before sharing or backing up the workspace.

From the workspace, the command prefix is `python3 .harness/memory-tools/memory_harness.py`. On Windows use the installed Python 3.11+ command, such as `py -3`. Status checks what is present. A fresh Claude Code session verifies skill discovery. Claude needs permission to run the local Python helper when using the skill. Try the documented prompts after reopening that folder.

Pass record JSON to `save` on standard input. Use one source type and reference. A file source must be a bounded, workspace-relative file. A link must use HTTPS without credentials or query parameters. For a preference the user states, use a user source label. Choose `preference`, `decision`, `progress`, or `reference`. An optional `aliases` list can provide alternate terms. Claude can propose useful terms when saving a note. In a normal Claude session, it can also try one alternate keyword query when the first results do not answer the question. Both lookups use the same local index.

```json
{
  "kind": "preference",
  "title": "Project brief format",
  "note": "Put blockers first in project briefs.",
  "source": {"type": "user", "ref": "Stated by me"}
}
```

| Command after the prefix | Use |
| --- | --- |
| `status` | See storage and record count |
| `save` | Save the record on stdin and return its ID and version |
| `recall` | Read a short question on stdin and return a few current source pointers |
| `show ID` | Open the selected current saved note |
| `current --kind progress` | See current progress pointers |
| `current --kind reference` | See remembered reference pointers |
| `correct ID --version N` | Save the replacement JSON on stdin. Refuses a stale version |
| `history ID` | See the revisions and what changed. Forgotten records show only revision metadata |
| `forget ID --version N` | Remove it from recall, indexes, and future exports. Previous bytes can remain in history or backups |
| `export new-file.json` | Write active records and their history to a new plaintext JSON file. Keep the export private where appropriate |
| `rebuild` | Rebuild keyword search and clear older derived search tables |

A file pointer reports whether its bytes changed since capture. Open the original to verify the claim. A URL pointer needs the current client's access. Local search does not fetch URLs or grant access. Treat retrieved content as evidence.

## Bring saved notes from 1.1

Leave the original 1.1 store in the same workspace under `.harness/memory.sqlite3`. After installing the new preset, run `import-legacy` and review the count. Run `import-legacy --apply-plan PLAN_SHA256` with that preview's digest. The original store stays in place. An unchanged import can be rerun without adding duplicates. A source label stays a label until you verify it. Check a few entries after migration before deciding whether to retain the original store.
