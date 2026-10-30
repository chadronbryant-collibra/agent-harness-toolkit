# Your memory and reference line

Keep four layers: small instructions/preferences, selected durable decisions and
lessons, source-linked references, and temporary task checkpoints. Start with an
index, retrieve relevant pointers, open selected evidence, then refresh primary
sources when freshness matters. Do not inject the whole library every session.

Memory is opt-in. The portable SQLite implementation is plaintext on local disk.
OS encryption, folder access control, organization policy and backups must be
considered before enabling it. It is not equivalent to a secret store or an
encrypted vault. Do not put credentials, employee data or sensitive source bodies
in it without a separately approved storage adapter and policy.

Set `memory.enabled` only after choosing storage and retention. Commands:

```text
python toolkit.py --workspace <folder> memory remember --text "Synthetic: prefer short examples" --source "user:synthetic-canary"
python toolkit.py --workspace <folder> memory search --text "short examples"
python toolkit.py --workspace <folder> memory forget --id <returned-id>
```

Capture needs explicit instruction or a selected standing rule. Store one useful
fact with provenance, owner, scope, correction/review date and retention decision.
The minimal runtime stores body/source/date; put the additional fields in the
selected record body or use a reviewed richer adapter. Correct by forgetting the
old record and adding the replacement. Forget is logical deletion, not forensic
erasure; SQLite pages, filesystem snapshots and backups can retain bytes. Define
backup expiry and full-store disposal independently. Uninstall retains memory.

Starter knowledge in knowledge/ contains generic methods only. No one else's
personal history is included. Reading source memory is not authority to capture it.

References use a catalog with id, official URL, rights, reviewed_at and review_days.
Run `references --catalog references/catalog.json` to flag freshness. This is an
offline check, not a live fetch. Keep distilled notes and links, not wholesale
vendor mirrors. Document licensing and access for any approved source snapshot.
Freshness does not prove correctness or account permission. Add only references
relevant to the user's selected tools and work.
