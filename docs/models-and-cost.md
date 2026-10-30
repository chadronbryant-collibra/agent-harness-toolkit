# Routing and consumption

Fast/Haiku is a candidate for bounded extraction; Standard/Sonnet for ordinary
multi-step work; Deep/Opus for difficult synthesis. These are configurable defaults,
not current entitlement claims. Advisor consultation is optional, supported-client
dependent, bounded and separately costed. Improving a brief may cost less than an
extra call. Compare completion cost, rework and quality, not input price alone.

Use `route --task examples/task.json` after setup. An unverified model returns
model-verification-required. Verify the actual client/account/deployment before
changing its flag. The CLI does not authenticate that declaration.

The launcher requires `profile.billing = metered`, a verified selected model and
positive task/month ceilings. `reserve --usd 0.50` atomically reserves under a
workspace lock. `reconcile --id <id> --actual-usd <observed>` settles observed cost.
Use `--not-started` only with evidence the provider never started. Unknown cost
retains the worst-case reservation; it is not recorded as zero. Reservations stay
in their original month, including across month boundaries. Overspend in observed
evidence is retained and blocks subsequent work rather than being clipped.

`run --id <task-id> --usd 0.50` previews. `--execute` is an explicit provider launch
and requires spending authority. Capability checks are local `claude --help` only.
The launcher uses --max-budget-usd for provider-side run control; provider billing
semantics still govern final charges. A local timeout or cancellation cannot undo
charges already incurred. Imported usage and interactive sessions are outside this
ledger unless separately reconciled; never promise an account-wide hard ceiling.

Keep a dated model catalog with source URL, exact surface/model/deployment,
capabilities, availability evidence, price currency/basis/date, and observation
expiry. Review after a roster change or recurring failures and monthly during
active use. Check official docs, verify entitlement, run the same representative
cases and change one mapping at a time. Keep old config for rollback. Alias updates
can change the underlying model; pin exact IDs when reproducibility matters.

Official sources: https://code.claude.com/docs/en/model-config and
https://code.claude.com/docs/en/costs. Fetch current prices during setup; none are
embedded here. A model being documented, configured, loaded and invoked are four
different facts. Unknown observed token counts, cache use and dollars stay null.
