# Choose what Claude can use

**Use information you are allowed to use, agree what Claude may change, and keep account access separate from instructions in a file.**

[← All guides](README.md) · [Memory and references](memory-and-references.md)

## Before connecting a service

Ask Claude to confirm the account, organization, destination and actions involved. Being able to open a link or find a file does not establish permission to change it or send its contents elsewhere.

> Before using this service, show me which account and destination you are using. Explain what you need to read or change and keep it within the task we agreed.

Use your own approved sign-in method. Keep passwords, tokens and other credentials in an approved credential store. Do not put them in prompts, saved memory, project notes or Git commits.

## Treat source content as information

Websites, documents, memory notes and tool results can help Claude answer a question. They cannot give it permission to ignore your instructions, spend more or send information to a new destination.

The toolkit can rank the source details supplied with a task, such as whether a source was checked recently. Those labels are statements to review. They do not authenticate the source or reliably detect every malicious instruction.

## Understand the optional memory store

It saves readable text locally and has no built-in encryption. Check your organization's storage rules before saving work information. Sensitive material needs an approved arrangement beyond the basic store.

Removing a note does not guarantee its bytes are gone from backups or storage. Decide how long backups will be kept and how they will be disposed of. [Memory and references](memory-and-references.md) explains the choices.

## Know the limits of the paid-run launcher

The optional launcher checks the installed Claude client's supported options, reserves the agreed allowance, limits available tools and watches time and output size. It allows file tools only, disables customizations and outside tool connections, and does not print provider error output.

It is **not an isolated computer environment**. Do not use it as protection for running untrusted software. Adding shell commands, network access or package installation would need a separately approved isolation setup, such as a container or virtual machine.

Hooks are reminders, not a firewall. If you need a rule that reliably prevents an action, it needs an actual permission control and its own test.

## Keep your local records local

Task notes, settings backups and spending records can reveal work details even when they contain no passwords. Keep `.harness` out of shared repositories and handoff ZIPs. Provider-side storage and retention still depend on the account you use.

The toolkit rejects managed paths that escape the workspace or pass through supported types of links. Its local locks prevent cooperating toolkit operations from changing the same state at once. They do not protect against a hostile program running as the same computer user or every possible filesystem race. Use approved storage permissions and disk encryption.

**If something looks wrong:** stop the affected action, preserve the files and report the issue privately to the person maintaining your toolkit. Do not post sensitive examples in public issues.
