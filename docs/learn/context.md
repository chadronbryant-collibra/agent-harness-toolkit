# Save a preference and find it again

## Open the download in Claude

1. Download the toolkit ZIP and extract it. In the Claude desktop app, open the **Code** tab and start a **Local** session. Choose the folder you just extracted. [Claude Code desktop guide](https://code.claude.com/docs/en/desktop)
2. Tell Claude where you want to keep your own work. You can choose an existing folder or create a folder called **My projects** for practice.

> Help me add memory to my **My projects** folder. Follow START-HERE.md from this download and show me what you’ll add.

Claude checks for Python and previews the setup. If Python is missing, ask Claude to guide you through the [official Python download](https://www.python.org/downloads/) before continuing. If Claude asks permission to run a command, check that it describes the toolkit helper and the folder you chose. At the end, ask Claude to give you the name and location of your work folder.

## Save something and come back

1. Start a new Local session and open **My projects**, the work folder you chose. Say **“Remember that I like project briefs to start with blockers.”** Wait for Claude to say it saved the preference in that folder.
2. Start another new Local session in **My projects** and ask **“How do I like my project briefs?”** Claude should answer “Put blockers first” and tell you it came from your saved preference.

If Claude can't find it, check the folder shown in the session. Ask **“Use workspace-memory to check if my preference was saved in this folder.”** If Claude can't run the helper, it should tell you that memory is unavailable for that session. Your notes stay in the work folder you chose. They are readable files on your machine, so keep private or sensitive information out of this storage.

To update an existing 1.2.0 setup, open the new download and ask **“Update the toolkit memory tools in my existing work folder. Show me the preview and keep my notes and edits.”** The setup recognizes the original 1.2.0 helper files and keeps edited copies for review.

## Keep project context and references

Use the [context starter](../../templates/context) to keep a short project update, next action, and links. Keep a few sources in [the reference index](../../templates/reference-library/SOURCES.md). You can place those files in your workspace or version the reference library in its own repository. Give each source a name, what it answers, and a review date.

> Read the project context and open the source it points to. What should I do next?

When you save a decision with a source link, Claude can check whether the source changed before relying on it. Plain context files work even when searchable memory is off. [Check a connection](connections.md)

## Try search by meaning

Try this after ordinary memory works. Search by meaning helps when the words you remember are different from the ones you saved. It needs Ollama and a small downloaded model on your computer.

> Help me try search by meaning in this work folder. Check whether Ollama is running locally with cloud features off. Guide me through anything missing, then let me choose the first note to include.

Claude can check the local runtime and identify the model. If it needs a download, it should show you [where to get Ollama](https://ollama.com/download) and which model to download. It should confirm which notes you want included before preparing them for search. Try a harmless example. Save **“Registration opens after the venue confirms capacity”** and add just that note. Then ask **“When can people sign up?”** Claude should locate the note and tell you which search it used.

You can say **“Turn off search by meaning for this folder.”** Keyword search still works when meaning search is off or the model is unavailable. [Exact commands and local setup](../reference/memory.md#search-by-meaning)
