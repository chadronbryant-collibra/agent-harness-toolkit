# Architecture and growth

One Python standard-library core owns portable mechanics. PowerShell and POSIX
launchers forward arguments without evaluating them. Model providers, clients,
storage and external services remain independently verified boundaries.

The user's workspace holds `.harness/config.json`, task checkpoints, usage and
optional memory. None belongs in the toolkit source or colleague ZIP. Instructions
and selected agent templates are installed at project scope only. Setup refuses
overwrites; uninstall removes only unchanged owned files. Hook changes have their
own digest-bound backup and rollback. Keep backups private: existing settings may
contain organization-specific information.

Intent assessment covers outcome, ambiguity and acceptance. Authority assessment
covers requester, effect and destination. Evidence assessment covers provenance,
freshness and conflicts. Routing covers completion demand, model availability,
capability and cost. These are separate dimensions; confidence never authorizes
effects. The CLI checks declared origin/effect and task fields; a caller-controlled
JSON field is not authenticated user identity. `assess --task <file>` ranks declared
source metadata as current-primary, current-reference, stale/undated or unverified;
every source retains zero instruction authority. Metadata is a review aid, not
proof of authenticity or a semantic prompt-injection detector. Client permissions and organizational
controls remain the enforcement boundary.

Interactive task loop: understand, plan, execute, verify, repair and deliver.
The task record supports resumable checkpoints and cycle limits. Its status is
executor-declared, not an independent grader. `agents` lists known task records,
not a census of all running provider agents; process state stays not-observed.
One metered restricted launch runs Claude's own internal agent loop under client
dollar limits and a wall/output budget. It does not implement an outer retry agent.

Improvement loop: select evidence, identify a failure/invariant, propose a scoped
change, reproduce, fix, check and measure later outcomes. The owner reviews policy,
permission, budget and retention changes. The workflow lives in skills/harness;
it never auto-captures memory or self-modifies routing from one result.

Future adapters must declare interface version, source/version binding, effects,
identity/destination checks, timeout, cancellation, privacy, accounting, uncertain
effect recovery, rollback and uninstall. Validate an adapter before adding it to
the manifest. Add encrypted storage, semantic search, additional providers or
scheduling through these interfaces without replacing the source of truth.
