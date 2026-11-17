# Local Memory Harness commands

Use this reference when you want exact commands, want to migrate, or want search by meaning. For everyday setup, start in [the short guide](../learn/context.md).

## Set up and use memory

Run these commands from the extracted toolkit, using the actual folder and the reviewed digest. Create the target folder first if it is new.

```text
python3 kit.py --workspace "/path/to/work" add memory-harness
python3 kit.py --workspace "/path/to/work" add memory-harness --apply-plan PLAN_SHA256
```

The preset installs the workspace-memory skill, its local scripts and settings, and an ignore rule under `.harness/`. It doesn't create a database until a memory operation needs one. It preserves existing files. If your target already has a different file at a planned path, review that conflict before making the smallest needed change. Use the separate `context` and `references` presets if you want starter files for either. Review the exact paths before sharing or backing up the workspace.

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

The optional adapter uses a local Ollama process and a downloaded embedding model. Check the [vendor setup](https://docs.ollama.com/faq) for your system, and choose whether to install it. Run it on your machine bound to `127.0.0.1` with Ollama cloud features disabled. Keep this service accessible only on the local machine. The toolkit connects directly to loopback and checks the selected model's full digest and local GGUF format. The API cannot attest the process settings. Use an instance you control with cloud disabled.

For a small English-language starter model, review [all-minilm](https://ollama.com/library/all-minilm) and download it separately. A model download uses the internet and disk space. The toolkit does not install Ollama or download models. Once installed, inspect the model's full digest in the local `GET /api/tags` response. Supply the exact local name, such as `all-minilm:latest`, and its full digest.

```text
semantic-configure --model all-minilm:latest --digest FULL_DIGEST
semantic-build --id RECORD_ID
recall --semantic
semantic-off
```

Use the same memory command prefix. Repeat `--id` to select several items, or use `--all` only if you intend to index all active notes in that workspace. Index building sends the selected note titles and text to that local model. Hybrid recall sends the query to that model and combines candidates with keyword results. The adapter never crawls a reference folder or downloads source files. The index supports up to 200 selected notes. New or corrected notes need an index refresh before meaning search can find their new content. Forget removes its matching vector. `semantic-off` removes the saved settings and vectors. If the model is unavailable or changed, the query falls back to keyword search and reports why. Local indexing and search make no Claude calls. Using the results in a normal Claude conversation follows the account's billing.
