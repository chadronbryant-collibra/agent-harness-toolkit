# Instructions for people and agents changing this toolkit

Keep the kit understandable, portable and safe to hand to someone starting fresh. Read [START-HERE.md](START-HERE.md) and [How the toolkit works](docs/architecture.md) before changing behavior.

## Keep the reader in view

Lead guides with what the person wants to do, a useful prompt or example, the choices that matter and what a good result looks like. Put exact commands in the clearly labeled reference area. Use ordinary language, explain necessary terms and preserve material limits beside the relevant action. Never describe a planned feature as working.

## Preserve work and access

Preserve user and peer files. Work on a purpose-specific branch. Keep credentials, private workspace records, transcripts, account identifiers and vendor-document copies out of the source and handoff. Use fictional examples.

Do not silently raise budgets, widen permissions, install connections or save memory from task content. External publication, invitations and paid calls need the authority for that action.

## Keep one implementation

Use Python 3.11+ and the standard library for the portable core. Keep platform launchers small and pointed at that same implementation. Preserve the versioned manifest, changelog, documentation and compatibility checks.

## Verify the claim you make

Before delivery, run:

```text
python -m unittest discover -s tests -v
python toolkit.py self-check
python scripts/package.py --output <new-archive-outside-the-repository.zip>
```

Source tests, a built package, installed files, fresh client loading, an actual invocation and the person's acceptance are different checks. Report only the stages observed. Windows support or a working account must be checked on that actual surface.

See [Check your setup](docs/acceptance.md) and [the command reference](docs/reference/commands.md).
