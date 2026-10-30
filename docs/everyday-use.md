# Get useful work done with Claude

**Tell Claude what you want to finish, give it the right sources, and agree what a good result looks like.** You can do this in ordinary language.

[← All guides](README.md) · [Models and cost →](models-and-cost.md)

## Start with a real outcome

“Help with this project” leaves a lot for Claude to guess. A clearer request names the result and the information it should use.

> Create a one-page project brief from these three notes. Keep the notes unchanged. Include the purpose, decisions, next actions and anything still unclear. Show where each action came from.

You do not need to prescribe every step. Give Claude enough context to make routine decisions and finish the work.

## Choose the kind of help you want

| If you need… | You can say… |
| :--- | :--- |
| Advice before deciding | “Compare these options, explain the tradeoffs, and recommend one. Wait before making changes.” |
| A finished draft | “Create the draft, check it against these sources, and bring me the result.” |
| Help carrying out a change | “Make this change in the files we agreed. Check the result and explain anything still unresolved.” |
| Another pair of eyes | “If it would help, use one reviewer with a clear task. Check its findings before changing the work.” |

An agent is another assistant given a specific piece of work. It can help with an independent review or a separate task, but it adds cost and coordination. Small tasks usually stay with the current Claude session.

## Give the work a finish line

Before a larger task, agree on:

- **The result:** what you want to receive.
- **The sources:** which files or information Claude should use.
- **The changes:** what it may edit, and what it must preserve.
- **The checks:** how you will know the result is right.
- **The limits:** when it should stop because of cost, missing information or a decision only you can make.

Claude should continue through the agreed steps without asking you to prompt every routine action. It should ask when a missing fact would materially change the result or require permission you have not given.

## Pick up where you left off

Before stopping a longer task, say:

> Save a short progress note with the goal, decisions, files changed, checks completed and what remains. Include anything we need to inspect before trying again.

When you return:

> Read that progress note and the current files. Tell me what still needs doing, then continue within the same scope and budget.

That progress note is a **checkpoint**. It helps a later session resume without rereading the whole conversation. It does not prove a background task has stopped or that a previous change succeeded.

## Learn from a completed task

> Review this result for one improvement we can reuse. Explain what happened, what supports your conclusion, and how we could check whether the change helps next time.

Claude can fix already-approved problems. Changes to spending limits, permissions or what gets remembered need your agreement. A useful lesson is worth keeping; the whole conversation usually is not.

**A good finish:** you have the result, know what was checked, and can see any remaining decision or limitation.

[Need help with an interrupted task? Open Maintenance](maintenance.md#when-work-stops-unexpectedly).
