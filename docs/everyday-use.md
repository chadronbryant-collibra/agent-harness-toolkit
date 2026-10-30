# Everyday work

Give Claude an observable outcome, sources, exact write scope, acceptance checks,
budget and stopping condition. Example: “Create a project brief from these three
notes. Keep notes unchanged. Every action needs a source. Finish the draft and
verify coverage; ask only if a missing fact changes the result.”

Use an advisory request for options before committing: “Assess these approaches,
rank by evidence, cost and maintenance, and recommend one. Do not implement yet.”

For a larger authorized task: “Implement this in an isolated worktree. Use one
read-only reviewer if useful. Own integration and verification. Stop if the named
budget or scope would be exceeded.” Verify actual client roles and model support.
Subagents cost tokens too; sequential dependent work usually stays inline.

Create a task record with `task --input examples/task.json`. Save progress with
`checkpoint --id <id> --status working --evidence "Source pointers and remaining checks"`.
Valid transitions are planned→working/blocked, working→working/blocked/verified,
blocked→working, verified→delivered. Working cycles are bounded. Evidence text is
executor-declared. Use private relative pointers, never secret bodies. `agents`
lists known records; it does not establish live process ownership.

To resume, read the exact checkpoint and current artifacts. Preserve objective,
authority, completed work, owned files and unresolved effects. Reconcile uncertain
writes or process state before retrying. An unchanged denial ends that route.

After useful work: “Review this selected outcome for one reusable improvement.
Separate observation, cause hypothesis, fix, reproduction and verification. Apply
already-authorized fixes; propose changes to permission/budget/memory policy.”
Use skills/harness/SKILL.md. Do not convert every conversation into durable memory.
