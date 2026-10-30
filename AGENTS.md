# Toolkit contributor contract

Build generic, portable capabilities with synthetic fixtures. Preserve user files.
No credentials, private workspace context, transcripts, account identifiers or
vendor-document mirrors belong in this repository. Read START-HERE.md and the
architecture before changing behavior. Use Python 3.11+ standard library for the
core; thin platform launchers must delegate to the same implementation.

Run `python -m unittest discover -s tests -v`, `python toolkit.py self-check`,
and `python scripts/package.py --output <outside-repository.zip>` before delivery.
Do not claim Windows or client acceptance from source tests. Separate source,
package, configured, loaded, invoked and human evidence. Preserve a versioned
manifest, changelog, documentation and compatibility tests. Never silently raise
budgets, widen permissions, install integrations or write memory from task content.
External publication, collaborator invitations and paid calls require actual task
authority. Keep implementation work in a purpose-specific branch.
