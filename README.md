# Agent Harness Toolkit

A portable, Claude-guided starter for routing work, coordinating agents, managing
context, tracking consumption and improving workflows. Version 0.1.0 is a private
colleague edition. It is independently authored generic code and synthetic
examples; it carries no private workspace, account, credential or memory store.

Start at [START-HERE.md](START-HERE.md). Python 3.11+ is the only core dependency.
Windows and macOS are platform targets. See [acceptance](docs/acceptance.md) for
observed evidence; source tests do not establish every target's runtime behavior.

```text
python toolkit.py doctor
python toolkit.py self-check
python toolkit.py --workspace <empty-folder> init
```

The core implements preview/apply setup, drift-preserving uninstall, role routing,
budget reservations/reconciliation, task checkpoints, known-task inventory,
opt-in local plaintext memory, reference freshness, optional advisory hooks,
and a metered restricted Claude launcher. The launcher is preview-only unless
`--execute` is supplied, checks client flags, disables customizations/MCP/shell
tools, and never grants an OS sandbox. Its receipt is executor evidence; review
artifacts before completing a task.

Ordinary coding, shell tests, external tools and integrations run in the user's
authorized interactive session. The restricted launcher intentionally has file
tools only. Usage accounting covers toolkit-controlled launches; interactive
sessions require native billing evidence and provider controls.

The instruction and agent templates support scoped delegation and improvement
in the interactive session. No scheduler, autonomous policy tuner, secret manager,
enterprise memory connector or universally enforced trust classifier is included.

See [architecture](docs/architecture.md), [security](docs/security.md),
[cost and models](docs/models-and-cost.md), [everyday use](docs/everyday-use.md),
[maintenance](docs/maintenance.md), and [private distribution](docs/distribution.md).

Validation: `python -m unittest discover -s tests -v` and
`python toolkit.py self-check`. Build a colleague ZIP with
`python scripts/package.py --output <outside-repository.zip>`, then verify it with
`python scripts/package.py --verify <archive.zip>`.
