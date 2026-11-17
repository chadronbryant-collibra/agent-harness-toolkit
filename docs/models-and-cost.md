# Choose the right help for the work

**Start with a capable everyday model. Use a lighter or deeper option when the task gives you a reason.** The aim is a useful result at a sensible total cost.

[← All guides](README.md) · [Everyday use](everyday-use.md)

## Ask Claude to help you choose

> Review the work I want to do and the models available in my account. Recommend an everyday option, a lighter option for simple tasks, and a deeper option for difficult work. Explain when you would switch and what that means for spending.

The toolkit uses three roles. Their starting model names are suggestions; Claude needs to check what your account can actually use.

| Role | Good starting use | Suggested model family |
| :--- | :--- | :--- |
| **Fast** | Find a fact, extract a short list, or organize a straightforward set of items. | Haiku |
| **Standard** | Draft, research, debug, or complete a task with several steps. | Sonnet |
| **Deep** | Work through a difficult problem with connected decisions or conflicting information. | Opus |

A more expensive model is not automatically the best choice. A clearer request can prevent unnecessary retries. For difficult work, finishing reliably can be cheaper than repeating a failed attempt with a lighter model.

## Set limits you understand

Agree how much you are comfortable spending on one task and over a month. Also decide when Claude should ask before using another agent or a more expensive option.

> Keep routine work on my everyday model. Before adding another paid agent or moving to a more expensive option, explain why it would help and how it fits the limit we agreed.

The sample amounts in the files are **examples**, not a spending decision made for you.

## Know which spending is covered

| How you work | What controls spending |
| :--- | :--- |
| You work in a normal Claude conversation | Your account's billing settings and the choices you agree with Claude. |
| You explicitly use the toolkit's paid-run launcher | The toolkit reserves a task allowance, checks its local budget record, and passes a run limit to the supported Claude client. |

The launcher is an optional way to start a limited paid task. It supports accounts billed for use, rather than subscription-only work. It allows reading and editing files, but does not run shell commands, connect tools, or delegate to more agents.

**A toolkit limit is not an account-wide spending cap.** Other conversations and services can incur costs outside its records. Check your provider's account controls as well.

Run `toolkit.py doctor` to see which bundled commands can spend. Local commands, including `reserve`, `reconcile`, and the optional `kit.py` helpers, only update or inspect files. Using a skill through Claude uses your normal session. Memory keywords and optional local embeddings make no Claude calls. Meaning search uses the separately installed local model. The metered launcher previews its allowance and covered file tools before execution, checks the workspace budget again when reserving, and rejects requested tools outside that coverage. You can narrow the file tools with the optional `tools` list in a task. Any added service needs its own billing scope, limit, and usage evidence before use.

## Make sense of a spending report

- **Reserved:** money set aside for a task that may still be running or needs a final check.
- **Observed:** a cost returned by the provider or supported by a usage record.
- **Unknown:** no reliable final amount is available yet. It must not be presented as zero.

If a run ends without a reliable cost, its reserved allowance remains counted until the outcome is checked. Ending a local process does not undo charges already incurred. A reservation keeps its original month, even if the task finishes later. If the provider reports a cost above the reservation, the toolkit records the full cost and flags it in the run receipt.

## Review the choice over time

After a model changes, repeated retries, or a month of regular use, ask:

> Compare completion quality, retries and spending for similar tasks. Recommend one model-setting change, explain the evidence, and keep the previous setting so we can reverse it.

Claude should check current availability and prices rather than rely on an old model name or price list. The kit includes a catalog template to help record that information.

[Configuration explained](reference/configuration.md) · [Commands for Claude](reference/commands.md#choose-and-preview-a-task) · [Official model settings](https://code.claude.com/docs/en/model-config) · [Official cost guidance](https://code.claude.com/docs/en/costs)
