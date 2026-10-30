# Maintain and grow the harness

After client/model changes, repeated failures, or monthly during active use:
run doctor; inspect affected model availability and official docs; review usage,
rework and outcomes; check reference freshness; review selected plugin/hook load
evidence; verify retention/backup choices; update one mapping at a time.

Update workflow: download a versioned private ZIP, verify its out-of-band digest
and internal file manifest, unpack beside the current version, run tests and
self-check, preview selected configuration/instruction changes, preserve owner
edits, activate in one project, and verify fresh client load. Switch hook absolute
paths only through a reviewed merge. Keep the previous version and config until
acceptance. Do not run `init` over an existing workspace to update it.

Rollback: restore the reviewed previous config; remove hooks through their
digest-guarded rollback or selectively merge after drift; restore previous
instructions from version control. Uninstall removes unchanged setup-owned files
only. It retains modified instructions, task receipts, budget records and memory.
Memory deletion/backup expiry requires the user's separate explicit action.

Run ownership: `.harness/active-run/owner.json` identifies one launched task and
reservation. A marker after interruption means unresolved, not dead. Inspect the
exact PID/process start and any possible effects before resolving budget and
removing the marker. PIDs can be reused. A missing process view is inconclusive.
An operation.lock after a crash likewise needs inspection; never auto-steal it.

Use an improvement packet with objective, sources, invariant, expected/observed,
cause confidence, scoped fix, known-bad test, verification and next outcome review.
Policy changes need review. Do not add unbounded watchers, queues or self-modifying
rules merely to make the system seem autonomous. New schedules require authority,
budget, cancellation, quiet/no-change behavior and failure notification design.
