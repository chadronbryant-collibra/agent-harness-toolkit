# Add tools deliberately

Use the smallest surface: documentation for a fact, a skill for a workflow, a tool
for deterministic mechanics, an agent for a separately scoped role, a hook for a
lifecycle event, MCP for structured client tools, and a plugin for distribution.
One canonical source should feed each client adapter. A copied file does not
prove discovery; an enabled plugin does not prove invocation.

Foundation needs Python. Git adds versioning and worktrees. GitHub CLI adds remote
repository and PR workflows. Node supports selected JS tools and MCP servers.
PowerShell supports Windows automation. Provider/cloud/database CLIs are optional
and should be installed only for a selected task. Present a small relevant menu,
verify official installers/versions, then test one bounded operation.

For GitHub: choose owner and private repository, verify `gh auth status` metadata
without printing credentials, verify origin and branch, then follow the user's
review rules. Never copy the maintainer's GitHub App, token or account config.
Repository creation and collaborator invitations are separate authorized effects.
Windows and macOS use their supported authentication routes.

For each integration record source/version/digest, license, supported clients,
install scope, tools/effects, authentication method, destination, data handling,
cost, timeout, rollback and uninstall. Pin executable dependencies and avoid
unreviewed install scripts, ambient npx latest, or unlimited shell permission.
Test source→package→configured→loaded→invoked separately in a fresh session.

The kit ships no MCP credentials, plugin marketplace install or external adapter.
To use the bundled workflow as a project skill, place the canonical
skills/harness/ directory in the client's verified project skill location after
checking for collisions; use that single intended route. Additional client
adapters must be tested rather than inferred from shared Markdown.
