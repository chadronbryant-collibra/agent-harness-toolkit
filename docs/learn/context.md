# Pick up where you left off

Copy the two Markdown files from [templates/context](../../templates/context) into a `context/` folder in your workspace. Keep existing files with the same names. Use `PROJECT.md` to record the outcome, current work, and next step. Use `PREFERENCES.md` for a few things you want the assistant to remember across sessions.

> Read context/PROJECT.md and open the sources it links to. Tell me what to do next.

Open a fresh session and try that prompt. If a source changed, use the new source and say what no longer matches the saved note. For regular use, ask Claude to add a short pointer to this folder in your existing project instructions. Only save a preference or decision you choose to keep.

## Start a reference library

Copy [templates/reference-library](../../templates/reference-library) to `reference-library/` in your workspace. Start with two or three sources. Add a link, what it answers, and when it was last checked. Keep your source files where they belong. You can use the same structure in a repository of its own once you need to share or version it.

> Read reference-library/SOURCES.md. Find the source that answers my question, open it if I have access, and show me where the answer came from.

Try [find-a-source](skills.md) if you want the same source check each time. Review dates are reminders to inspect a source. Sharing the index does not grant access to linked files.

## Add searchable memory

For a few notes, start with the files above. To search more saved items, the toolkit includes an optional local memory store. It saves short entries with source labels and searches for matching text. Use a harmless preference first, then check it in a fresh session and remove it if you want.

Ask Claude to open the [memory setup instructions](advanced.md#try-searchable-memory) and help you complete that first example. The store starts off and uses plaintext SQLite inside the chosen workspace. Choose what you can keep there, avoid secrets and sensitive notes, and keep the state out of shared repositories. This edition ships local memory commands. It does not connect to a private Memory Harness service or provide meaning-based search.

[Memory and references](../memory-and-references.md)
