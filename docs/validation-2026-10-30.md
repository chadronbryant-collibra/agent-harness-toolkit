# Validation observation — 2026-10-30

Observed on macOS arm64 with Python 3.14.6:

- 42 unit/integration tests passed, with ResourceWarning treated as error.
- Declared evidence ranks by provenance/freshness without changing effect authority.
- Positive/negative setup, scope, cost, memory, hook and lifecycle cases passed.
- Two real concurrent processes produced exactly one admitted budget reservation.
- A real synthetic subprocess returned bounded output and reconciled observed cost.
- A real sleeping synthetic subprocess was stopped by the wall-time limit.
- A malformed executor return was not treated as acceptance or zero cost.
- Deterministic ZIP bytes, archive integrity, unpack and self-check passed.
- POSIX shell bootstrap and zero-network doctor/self-check ran successfully.
- Installed Claude 2.1.303 help exposed required launcher flags. No live model
  invocation, account verification or paid call was performed for this validation.

Windows and other Python/architecture runners, PowerShell bootstrap, actual Claude
hook invocation, fresh agent/skill discovery, provider billing readback and colleague
acceptance remain pending. The CI matrix is configured, not an observed passing run.
The core memory option is plaintext; no encrypted-memory parity is claimed.
