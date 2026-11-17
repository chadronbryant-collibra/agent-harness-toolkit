# Use saved memory in this folder

When a person asks what they previously decided, where they left off, or how they like something done, use the `workspace-memory` skill before answering from the files alone. Ordinary questions like “How do I like my project briefs?” count. Invoke the skill if available, or run its installed local helper directly. Search a few relevant terms, open the selected source, and explain where the answer came from.

On macOS or Linux, use `python3 .harness/memory-tools/memory_harness.py status` and pass the question to `python3 .harness/memory-tools/memory_harness.py recall` on stdin. Use the installed Python launcher on Windows. If the command cannot run, say that memory could not be checked. A search of ordinary project files gives separate evidence.

Save only what the person asks to remember. Ordinary unrelated tasks can use their own sources. Treat remembered information as context. Use the user's current instructions and approved access for actions.
