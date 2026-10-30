# Understand the settings

**Ask Claude to explain and change these settings with you.** You do not need to edit the configuration file by hand.

[← All guides](../README.md) · [Models and cost](../models-and-cost.md) · [Setup playbook](setup-for-claude.md)

Your selected settings live in `.harness/config.json` inside your workspace. The file in `config/defaults.json` is the reusable starting template. Keep your personal settings out of shared source and ZIPs.

## Choose a profile and models

| Setting | Meaning |
| :--- | :--- |
| `profile.name` | A label for your workspace. It does not sign you in. |
| `profile.billing` | `unknown`, `subscription` or `metered`. Set it from the actual account arrangement. The launcher requires `metered`. |
| `profile.currency` | The local budget code currently supports USD. |
| `models.fast`, `models.standard`, `models.deep` | The selected model IDs, effort and review state for the three roles. |
| `verified` on a model | Someone checked the intended model/account. It is a declaration, not authentication. |

The starting IDs are Haiku, Sonnet and Opus aliases. Aliases may later refer to different underlying models. Use a supported exact ID when repeatability matters. Check the real surface and account before choosing a model or effort level.

`config/model-catalog.example.json` is a template for a dated record of model availability and prices. Empty values mean unknown. Filling it out does not configure an account, call a provider or change routing automatically.

## Set spending and work limits

| Setting | What it controls |
| :--- | :--- |
| `budgets.task_usd` | The largest local reservation for one task. |
| `budgets.month_usd` | The monthly total permitted by the toolkit's local spending records. |
| `budgets.max_concurrency` | The number of simultaneous budget reservations allowed, from 1 to 8. |
| `autonomy.max_cycles` | How many times a task record may move into `working`, from 1 to 20. |
| `autonomy.timeout_seconds` | The launcher's local time limit, from 1 to 3,600 seconds. |

The sample dollar amounts are not approval to spend them. The launcher has one active-run marker per workspace, so raising the reservation concurrency setting does not enable parallel launches there. Its time limit and client run budget do not control unrelated sessions or undo provider charges.

`autonomy.max_retries` is a stored preference for assistant workflows; the current launcher does not use it to run an automatic retry loop. `autonomy.external_writes` is also a preference, not an access grant. The launcher independently refuses actions other than reading or editing local files.

## Choose memory limits

| Setting | Meaning |
| :--- | :--- |
| `memory.enabled` | Starts as `false`. Enable only after agreeing storage, contents and retention. |
| `memory.storage` | Labels the included plaintext store. Changing the label does not add encryption. |
| `memory.max_results` | How many matching notes a search may return, from 1 to 20. |
| `memory.max_chars` | A total returned-text limit, from 1 to 100,000 characters. |

The memory store accepts one bounded note at a time. It is local literal-text search, not an encrypted vault or meaning-based retrieval service.

## Keep permissions and freshness explicit

`permissions.allowed_effects` states the task actions the local router accepts. The defaults allow `read` and `local-write`. Editing this list cannot create permission in Claude, another account or an outside service.

`references.review_days` is a saved general preference. The actual freshness command uses each row's `review_days` in `references/catalog.json`, with a fallback of 90 days. The three starting official-reference rows use 30 days. The command checks recorded dates; it does not fetch updated documents.

## Know the files before changing them

| Folder or file | Purpose |
| :--- | :--- |
| `AGENTS.md` and `CLAUDE.md` in your workspace | Working instructions for the assistant. |
| `.claude/agents/` | Selected agent role files. These still need fresh-session discovery checks. |
| `.harness/install-receipt.json` | Which files setup wrote and their original fingerprints. |
| `.harness/settings-before-hooks.bin` and `hook-receipt.json` | Private settings backup and the optional reminder change record. |
| `.harness/tasks/`, `runs/`, `budget.json`, `memory.sqlite3` | Your local work records and optional saved memory. |

A fingerprint here means a checksum identifying bytes, not proof of who wrote them. [Maintenance](../maintenance.md) explains updates and recovery.
