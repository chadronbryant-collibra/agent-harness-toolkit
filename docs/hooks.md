# Optional advisory hooks

The kit offers SessionStart orientation, PreCompact continuity and Stop evidence
reminders. They read a bounded JSON payload, retain none of it and make no provider
calls. They are advisory, not a security firewall or an automatic resume loop.
No prompt classification model runs on every hook.

Verify installed Claude support for command hooks with explicit `args` using the
current official reference: https://code.claude.com/docs/en/hooks. Preview:

```text
python toolkit.py --workspace <folder> hooks preview
python toolkit.py --workspace <folder> hooks apply --binding <preview-binding>
python toolkit.py --workspace <folder> hooks remove
```

Apply merges only these project handlers and preserves existing keys. The private
backup and receipt live in .harness. Remove restores the original settings only
when the installed bytes are unchanged; later owner changes require a selective
manual merge. Interrupted apply leaves a prepared receipt for inspection; do not
replay automatically. Keep the toolkit at its installed absolute location.

Test a synthetic payload locally, then verify actual event invocation in a fresh
client. Nonzero errors fail open as advisory hooks under client default behavior;
they do not grant permissions. No guard is claimed for connectors, shell commands
or secrets. Restricted launcher runs disable these and other customizations.
