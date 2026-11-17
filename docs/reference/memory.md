# Local Memory Harness commands

Use this reference when you want exact commands, want to migrate, or want search by meaning. For everyday setup, start in [the short guide](../learn/context.md).

## Set up and use memory

Run these commands from the extracted toolkit, using the actual folder and the reviewed digest. Create the target folder first if it is new.

```text
python3 kit.py --workspace "/path/to/work" add memory-harness
python3 kit.py --workspace "/path/to/work" add memory-harness --apply-plan PLAN_SHA256
```

The preset installs the workspace-memory skill, a project rule to use memory when relevant, the local scripts and settings, and an ignore rule under `.harness/`. It doesn't create a database until a memory operation needs one. It preserves existing files. The same preview updates untouched 1.2.0 helper files and keeps the existing store. Review any file conflict before applying a change. Use the separate `context` and `references` presets if you want starter files for either. Review the exact paths before sharing or backing up the workspace.

From the workspace, the command prefix is `python3 .harness/memory-tools/memory_harness.py`. On Windows use the installed Python 3.11+ command, such as `py -3`. Status checks what is present. A fresh Claude Code session verifies skill discovery. Claude needs permission to run the local Python helper when using the skill. Try the documented prompts after reopening that folder.

Pass record JSON to `save` on standard input. Use one source type and reference. A file source must be a bounded, workspace-relative file. A link must use HTTPS without credentials or query parameters. For a preference the user states, use a user source label. Choose `preference`, `decision`, `progress`, or `reference`. An optional `aliases` list can provide alternate terms.

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
| `status` | See storage, record count, and semantic status |
| `save` | Save the record on stdin and return its ID and version |
| `recall` | Read a short question on stdin and return a few current source pointers |
| `show ID` | Open the selected current saved note |
| `current --kind progress` | See current progress pointers |
| `current --kind reference` | See remembered reference pointers |
| `correct ID --version N` | Save the replacement JSON on stdin. Refuses a stale version |
| `history ID` | See the revisions and what changed. Forgotten records show only revision metadata |
| `forget ID --version N` | Remove it from recall, indexes, and future exports. Previous bytes can remain in history or backups |
| `export new-file.json` | Write active records and their history to a new plaintext JSON file. Keep the export private where appropriate |
| `rebuild` | Rebuild keyword search and clear the optional index so it can be rebuilt separately |

A file pointer reports whether its bytes changed since capture. Open the original to verify the claim. A URL pointer needs the current client's access. Local search does not fetch URLs or grant access. Treat retrieved content as evidence.

## Bring saved notes from 1.1

Leave the original 1.1 store in the same workspace under `.harness/memory.sqlite3`. After installing the new preset, run `import-legacy` and review the count. Run `import-legacy --apply-plan PLAN_SHA256` with that preview's digest. The original store stays in place. An unchanged import can be rerun without adding duplicates. A source label stays a label until you verify it. Check a few entries after migration before deciding whether to retain the original store.

## Search by meaning

Start with the [guided setup](../learn/context.md#try-search-by-meaning). Use the following for troubleshooting or if you prefer commands. Run them from the work folder with the installed memory command prefix.

```text
semantic-check
semantic-configure --use-by-default
semantic-build --id RECORD_ID
recall
```

`semantic-check` reports what's missing and the next step. It reads runtime metadata without sending saved notes. Use [Ollama's local-only setup](https://docs.ollama.com/faq#how-do-i-disable-ollamas-cloud-features) with the service bound to the local machine. The toolkit cannot verify the process's cloud settings through its API. Use a local instance you control and separate it from any shared instance.

The default model is [all-minilm:latest](https://ollama.com/library/all-minilm). Download it separately with `ollama pull all-minilm:latest` when you choose to use it. `semantic-configure` reads the local model fingerprint and records it for future checks. A different supported model or port can be selected with `--model` or `--port`. Model installation and updates can use the internet and disk space.

Repeat `--id` to include several saved notes. Use `--all` only if you intend to include every active note in this folder. Building replaces the prior selection and sends the chosen note titles and text to the local model. It handles up to 200 selected notes. After a change or correction, rebuild with the records you want included. A model change requires reviewing the new model and rebuilding.

With `--use-by-default`, a normal recall uses meaning search in this folder when ready. Use `recall --keyword-only` for a single keyword lookup or `semantic-off` to remove the meaning-search settings and index. Existing configurations without a default choice still use meaning search only with `recall --semantic`. Local search makes no Claude calls. Using the results in Claude follows your normal session billing.
