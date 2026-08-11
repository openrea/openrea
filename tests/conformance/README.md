# openREA Conformance (v0.1-draft)

Two levels. Level 1 is implemented here; level 2 is specified and stubbed.

## Level 1 — document conformance (implemented)

A document is conformant when it passes all of:

1. **Schema validity** against `schema/openrea.schema.json` (JSON Schema 2020-12, format-checked timestamps, string-decimal quantities, per-type strictness — unknown fields belong in `metadata`).
2. **Id uniqueness** across the record set.
3. **Referential integrity** — no dangling references, and references point at the right record type where the spec makes it unambiguous (`asserted_by` → agent, `settles[]` → commitment, `flows[].resource` → resource, …). SPEC §5.
4. **Supersession acyclicity.** SPEC §7.
5. **No contradictory accepted assertions** for the same `{record, attribute}` where neither is superseded. Identical claims are corroboration and pass. SPEC §5.

Run it:

```bash
python tests/conformance/validate.py --suite      # examples/ + valid/ must pass; invalid/ must fail
python tests/conformance/validate.py FILE.json    # validate any document
```

(Dev setup: `python3 -m venv .venv && .venv/bin/pip install jsonschema rfc3339-validator`, then use `.venv/bin/python`.)

### Fixtures

| fixture | expectation | rule exercised |
|---|---|---|
| `../../examples/*.json` | pass | canonical examples are normative |
| `valid/minimal.json` | pass | smallest useful document |
| `valid/duality-exchange.json` | pass | SPEC §4.9 duality — two event legs of one exchange (McCarthy 1982, Fig. 6) |
| `invalid/float-amount.json` | fail (schema) | SPEC §3.4 string decimals |
| `invalid/estimate-missing-basis.json` | fail (schema) | SPEC §9 / principle 13 |
| `invalid/agent-missing-operator.json` | fail (schema) | SPEC §4.2 principal reachability |
| `invalid/dangling-ref.json` | fail (integrity) | SPEC §5 |
| `invalid/cyclic-supersedes.json` | fail (integrity) | SPEC §5/§7 |
| `invalid/duality-non-event.json` | fail (integrity) | SPEC §4.9 duality must link two events |

## Level 2 — implementation conformance (specified, not yet implemented)

Per SPEC §12, a conformant *implementation* additionally answers four queries over any conformant record set:

1. **Open obligations** — commitments with derived status open/partially settled as of a date.
2. **Belief at T** — record state as of system time T (`recorded_at ≤ T`, supersession applied as of T).
3. **Why is this number here?** — full provenance traversal from a projection output to policy+version, calculation inputs, events, assertions (with approvers), and original evidence.
4. **Round-trip** — export per SPEC §11 and re-import with byte-identical projections.

Fixture harnesses for these are the next conformance milestone; the stablecoin example's non-normative `reference_projection` block is the seed for query 3.

Becoming a second implementation is meant to be a weekend project. If these fixtures make it harder than that, that's a bug — file it.
