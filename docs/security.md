# Security and trust boundaries

This is a local user-operated toolkit, not a sandbox, identity provider or tenant
permission service. Task origin and verified-model flags are declarations. User
and organization policy, native client permissions and destination verification
remain necessary. Content ranking never changes instruction authority.

No import or diagnostic starts a network connection, credential discovery or model
call. The only model route is explicit `run --execute`. It checks required CLI
flags, restricts tools, disables customizations and MCP, reserves spend, bounds wall
time/output, and retains ambiguous-run state. Authentication stays with the user's
installed client; the toolkit never reads or distributes credentials. Client-side
controls must be verified against the actual installed version.

The launcher permits file tools only. It is not suitable for untrusted repositories
requiring OS isolation. Use an approved container/VM sandbox before adding shell,
network or package execution. Relative scope instructions are not a filesystem
security boundary. Hook reminders are advisory, fail open, and never inspect or
log complete prompts. Guard hooks require a separately tested enforcement design.

Managed paths reject traversal, symlinks and (where supported) Windows junctions.
Local locks serialize cooperating toolkit operations; adversarial filesystem races
and hostile same-user processes are out of scope. File permissions differ across
OSes. Use approved local storage, ACLs and disk encryption. Memory is plaintext;
forget does not guarantee secure erasure. Backups need the same data boundary.

Receipts contain selected metadata, hashes and user-selected evidence pointers.
They can still reveal work patterns. Keep .harness out of source control and
shared ZIPs. Neither exception messages nor provider stderr are printed. Provider
output is transient and only its hash/cost metadata are retained by the launcher;
provider-side retention remains governed by the selected account policy.

Report defects privately to the toolkit owner through the existing delivery
channel. Do not post sensitive reproductions in public issues.
