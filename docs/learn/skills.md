# Add a skill for a task you repeat

A skill is a short set of instructions your assistant can follow each time you ask for the same kind of work. Start with one that matches a task you already do.

| If you want to… | Copy this folder from the toolkit | Try in a fresh Claude Code session |
| --- | --- | --- |
| Draft a short brief from your notes | [skills/write-a-brief](../../skills/write-a-brief/SKILL.md) | “Use /write-a-brief on these notes. Put blockers first.” |
| Find the source behind an answer | [skills/find-a-source](../../skills/find-a-source/SKILL.md) | “Use /find-a-source to check our publishing checklist.” |
| Get advice before you change something | [skills/review-a-plan](../../skills/review-a-plan/SKILL.md) | “Use /review-a-plan on this proposal and tell me what you’d change.” |
| Turn a repeated request into a skill | [skills/build-a-skill](../../skills/build-a-skill/SKILL.md) | “Use /build-a-skill on the request I give you.” |

In the folder where you work, put the selected skill folder inside `.claude/skills/`. For example, `write-a-brief` goes at `.claude/skills/write-a-brief/SKILL.md`. Ask Claude to show you the destination first. If that skill is already present, compare the copies before changing it. Reopen the folder in a new session and try the prompt. If the skill name is missing, check the folder and the client’s skill support.

## Get a second opinion

Use `review-a-plan` with a proposal and the decision you need to make. It can give advice in the current session. If you want a separate reviewer, specify the question and what files the reviewer may see. Ask the assistant to explain the extra usage and how it will check the review before relying on it.

## Make it yours

Copy [the skill template](../../templates/skill-starter/SKILL.md) to a folder named for your task. Change its name, describe when to use it, list the sources it should read, and write what a good result contains. Test it on one real example. You can also use `build-a-skill` to guide those edits.

To update or remove a skill, compare or remove only its own folder after saving changes you want to keep. A skill runs in your assistant session and uses that session’s billing.

[Claude Code skill locations and loading](https://code.claude.com/docs/en/skills)
