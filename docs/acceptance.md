# Acceptance evidence

Version 0.1.0. Record actual observations in a delivery receipt. Do not convert
an unrun item into a passing claim. CI configuration is not CI execution evidence.

| Surface | Required evidence |
|---|---|
| Python core | Positive and negative unit tests; duplicate JSON, scope/traversal, budget, lifecycle, drift preservation |
| Windows x64 | Real runner: setup, paths with spaces, locks, SQLite, subprocess cancellation, archive roundtrip |
| macOS | Same real platform suite and shell bootstrap |
| Windows/macOS arm64 | Native runner or attended device tests; not inferred from x64 |
| Package | Explicit allowlist, deterministic bytes, per-file hashes, verify/extract/doctor roundtrip |
| Claude | Required flag probe; fresh instructions/agents/skills load; real hook invocation; authorized bounded task |
| Memory | Explicit enablement, synthetic remember/search/forget, retention limits explained |
| Cost | Concurrent reservations, month boundary, unknown/observed reconciliation; actual billing readback separately |
| Recovery | Interrupted/ambiguous run retained; modified uninstall files retained; settings rollback refuses drift |
| Human | Colleague completes first useful task, resume, retrieval, update and uninstall walkthrough |

No live paid model call is required for source/package validation. Native client
and human acceptance stay pending until actually performed with the right account.
