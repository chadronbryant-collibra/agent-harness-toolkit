# Add what your work needs

**Start with the tools you already use. Add one new capability when you can name the task it will help you finish.** You do not need to install everything in this repository.

[← All guides](README.md) · [Check your setup](acceptance.md)

## Understand the options

| Name | What it means | Example |
| :--- | :--- | :--- |
| **Skill** | Instructions for a repeatable way of working. | A workflow for reviewing a project brief. |
| **Tool** | A program that performs a particular action. | Checking files or reporting task costs. |
| **Plugin** | A package that makes related capabilities easier to install in a supported client. | A set of skills for a particular service. |
| **Agent** | Another assistant given a clearly defined task. | Reviewing a draft without changing it. |
| **Connection** | A way for Claude to work with an outside service. Some use a standard called MCP. | Reading information from a service you have approved. |
| **Hook** | A reminder or action tied to a moment in a session. | Reminding Claude to save a progress note before it shortens the conversation. |
| **CLI** | A tool you can run from a terminal. Claude can guide you through it. | GitHub CLI for repository work. |

These serve different purposes. A skill can explain how to use a service, but it does not create an account or connect that service for you.

## Start with the task

> I want help with [task] using [service or files]. Review what I already have. Recommend the smallest useful addition, explain its cost and access needs, and show me how to try it safely.

Claude should check official installation guidance and confirm that the tool works on your computer. It should explain what will be installed, where it will apply, and how to remove it.

## Choose only the software you need

| If your work needs… | Claude may help you set up… |
| :--- | :--- |
| Local history and a way to work on separate changes | Git |
| A shared home for your project and reviews | GitHub, with GitHub CLI if useful |
| A selected JavaScript tool or connection | Node.js |
| Windows automation | PowerShell |
| A particular cloud service or database | That service's approved tool and sign-in method |

The setup guide covers the small amount of software the toolkit itself needs. You do not need to choose those technical details before talking to Claude.

## Add a capability in four steps

1. **Choose it.** Explain the job it should do and confirm the source is trustworthy.
2. **Review access.** Confirm the account, service, information and actions it will be allowed to use.
3. **Try it.** Start a fresh Claude session and complete one small, harmless task.
4. **Keep or remove it.** Record the working version and how to update, disconnect or uninstall it.

A plugin being listed as installed does not prove Claude loaded it or that its connection works. Ask Claude to show you the result of the small test.

## Set up GitHub when you need a shared project

> Help me create or choose a repository for this project. Confirm the account and repository name, explain who can see it, and show me how changes will be reviewed before they are merged.

Use your own account and approved sign-in method. Do not copy someone else's tokens or connection files. Creating a repository does not automatically give a colleague access; invitations are a separate choice.

## Use the included harness skill

The toolkit includes a workflow in `skills/harness/`. Ask Claude to install that skill in a supported project location, check for an existing copy first, and verify it appears in a fresh session. It is not automatically installed just because the folder exists.

**A good finish:** you know what was added, can show it working, understand its access, and can remove it.

[Optional reminders](hooks.md) · [Information and permissions](security.md) · [Maintenance](maintenance.md)
