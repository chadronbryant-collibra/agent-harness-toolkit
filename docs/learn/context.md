# Keep something useful and find it again

Open the extracted toolkit in Claude Code and try this prompt.

> Help me set up memory for this folder. Show me what you'll add. Then help me save one preference and find it in a fresh session.

1. Choose the folder where you want the memory. Claude shows the files it will copy and keeps your existing instructions. The helper needs Python 3.11 or later.
2. Say “Remember that I like project briefs to start with blockers.” Claude shows the saved preference and where it lives.
3. Open a fresh Claude Code session in the same folder. Say “Use workspace-memory. How do I like my project briefs?”

For a decision, save a note with its source. On recall, Claude opens the source through your approved access and can flag a change or a missing source. Ask before saving or correcting information. The toolkit's memory is plaintext on your machine. Use it for material suitable for that storage and keep the directory out of shared repositories and inappropriate backups.

## Keep project context and references

Use the [context starter](../../templates/context) to keep a short project update, next action, and links. Keep a few sources in [the reference index](../../templates/reference-library/SOURCES.md). You can place those files in your workspace or version the reference library in its own repository. Give each source a useful name, what it answers, and a review date.

> Read the project context and open the source it points to. What should I do next?

Open a fresh session to try it. Plain context files work even when searchable memory is off. The included brief and source-finding skills can use the same files. An existing Google Workspace or GitHub connection can open a source when the current account has access. [Check a connection](connections.md)

## Add search by meaning when it helps

Use keyword search for names, phrases, and saved aliases. If you often describe a topic in different words, ask Claude to help you enable [search by meaning](../reference/memory.md#search-by-meaning). You choose the local model and which saved items to index. Keyword recall stays available while the option is off or unavailable.

[Exact memory commands, import and recovery](../reference/memory.md)
