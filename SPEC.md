# openREA Specification — v0.1 (draft)

Status: **draft for adversarial review.** Nothing here is stable. Field names, semantics, and structure may change until v0.1 is tagged. The words **MUST**, **SHOULD**, and **MAY** are used as in RFC 2119.

---

## 1. Scope

openREA specifies a portable, machine-readable representation of economic activity: nine record types, their required semantics, identity and referencing rules, time semantics, assertion/supersession lifecycle, evidence and provenance rules, and the interfaces by which deterministic **projections** (GAAP, tax, ledger, management, audit) are derived from the record.

openREA does **not** specify: a database, a wire protocol, an agent framework, an application, or any particular accounting treatment. Those are implementations and consumers.

## 2. Design commitments

1. **Append-only.** Records are never destructively edited. Corrections are new records that supersede old ones (§7).
2. **Evidence-linked.** Claims trace to evidence and to the agent who asserted them (§8).
3. **Bitemporal.** The record distinguishes when something happened, when it takes economic effect, and when the system learned of it (§6).
4. **Accounting-agnostic.** Economic facts are stored once; accounting meaning is applied by versioned policies at projection time (§10).
5. **Judgment-honest.** Estimates and judgments are first-class assertions with a stated basis, never disguised as observations (§9).
6. **Rail-agnostic.** Settlement through ACH, card, wire, stablecoin, tokenized deposit, or machine-payment protocol changes the *evidence*, not the shape of the economic record.
7. **Portable.** A complete record set plus its evidence MUST be exportable in the documented format (§11), sufficient to reconstruct every projection.

## 3. Documents, records, identity

### 3.1 Document

An openREA document is JSON:

```json
{
  "openrea_version": "0.1-draft",
  "records": [ ... ]
}
```

Streams (JSONL, one record per line) are also conformant. Record order MUST NOT carry meaning; all relationships are explicit by reference.

### 3.2 Records

Every record has:

| field | req | semantics |
|---|---|---|
| `record_type` | MUST | one of the nine primitive types, lowercase |
| `id` | MUST | globally unique identifier (§3.3) |
| `recorded_at` | MUST | system time the record entered the store (RFC 3339 UTC) |
| `metadata` | MAY | implementation-defined object; consumers MUST tolerate unknown keys |

### 3.3 Identifiers

Identifiers MUST be stable and globally unique within a record set. RECOMMENDED: prefixed ULIDs (`evt_01J4Q2W9K3R8ZM5T`) with type prefixes `res_ agt_ evt_ cmt_ agr_ evd_ ast_ pol_ rel_`. Human-meaningful IDs (as in the examples) are permitted; uniqueness, not format, is normative. References to other records use their `id`; dangling references make a document non-conformant.

### 3.4 Quantities and money

Numeric economic magnitudes MUST be **string-encoded decimals** (`"2500.000000"`), never floats.

```json
{ "amount": "2500.00", "unit": "USD", "unit_type": "currency" }
{ "amount": "2500.000000", "unit": "USDC", "unit_type": "token", "token_ref": { "chain": "eip155:8453", "contract": "0x8335..." } }
{ "amount": "40", "unit": "hour", "unit_type": "quantity" }
```

`unit` is ISO 4217 for currencies; for tokens and other units it is a symbol whose meaning MUST be pinned by `token_ref` or resource definition.

## 4. The nine primitives

### 4.1 Resource
Something of economic value whose quantity, control, or condition can change: cash and deposits, tokens, receivables-as-rights, inventory, equipment, service capacity, licenses.

Required: `kind` (e.g. `fiat_deposit`, `token`, `inventory`, `right`, `capacity`), `unit`. Optional: `description`, `custody` (where/how held), `fungible` (bool), `external_refs`.

### 4.2 Agent
A party that participates in economic activity: people, legal entities, systems, **autonomous agents**.

Required: `kind` (`person` | `organization` | `system` | `autonomous_agent`), `name`. Optional: `identifiers` (jurisdictional/registry IDs), `operated_by` (agent ref — REQUIRED for `autonomous_agent`), `roles`.

An autonomous agent is a legitimate *asserter* and *participant* but never an *obligor of last resort*: obligations bind the principal named in the agreement, and `operated_by` MUST make that principal reachable.

### 4.3 Event
An occurrence that changed economic reality: purchase, delivery, payment, performance, receipt, transformation, adjustment, settlement.

Required: `event_type`, `occurred_at`, at least one of `flows` or `subject`. Optional: `effective_at` or `effective_period`, `participants` `[ { agent, role } ]`, `flows` `[ { resource, direction: increase|decrease|transfer, quantity, from_agent?, to_agent? } ]`, `settles` (commitment refs), `fulfills` (commitment refs), `evidence` (refs).

An event record is a *description*. Its canonical standing comes entirely from its assertions (§7): an event with no accepted assertion is a proposal, not a fact.

### 4.4 Commitment
A promised or obligated future event: a payment obligation, a performance obligation, a delivery promise.

Required: `commitment_type`, `obligor` (agent ref), `obligee` (agent ref), `terms` (quantity and/or resource), `due` (date or period). Optional: `agreement` (ref), `settlement_terms` (acceptable settlement forms).

Commitment **status is derived, never stored**: open, partially settled, settled, or cancelled is computed from the events whose `settles`/`fulfills` reference it and from superseding assertions. Storing status would create a second source of truth.

### 4.5 Agreement
The economic frame binding parties and commitments: a contract, an engagement, a subscription, an implicit trade custom made explicit.

Required: `parties` (agent refs). Optional: `commitments` (refs), `evidence` (refs to the executed contract), `effective_period`.

### 4.6 Evidence
An artifact supporting assertions. Evidence is **immutable**; better evidence supersedes via new assertions, never by editing.

Required: at least one identity anchor —
- `content_hash`: `{ "algorithm": "sha256", "value": "83af77..." }` for file-like artifacts (stored content-addressed, outside the record), and/or
- `external_locator`: for artifacts whose integrity is anchored elsewhere (e.g. `{ "type": "onchain_transaction", "chain": "eip155:8453", "tx_hash": "0x..." }`).

When both are present, the external locator is the identity and the content hash is the durability snapshot. Implementations SHOULD snapshot external artifacts content-addressed, because chains and URLs outlive neither subpoenas nor migrations equally well.

Plus: `mime_type` (when file-like), `source` (where it came from), `received_at`. Optional: `describes` (refs), `metadata`.

### 4.7 Assertion
A claim by an agent about a record or attribute. **Assertions are the only mechanism by which anything becomes canonically true in openREA.**

Required: `subject` (record ref, or `{ record, attribute }` pair), `asserted_by` (agent ref), `asserted_at`, `kind` (§9: `observation` | `estimate` | `judgment`), `status` (`proposed` | `accepted` | `rejected` | `superseded`). Optional: `claim` (the attribute values being asserted), `confidence` (0–1; meaningful mainly for machine asserters), `basis` (REQUIRED for `estimate` and `judgment` — the method and inputs), `evidence` (refs), `supersedes` (assertion ref), `approvals` `[ { agent, at, action } ]`.

### 4.8 Policy
A versioned, deterministic rule converting economic facts and accepted judgments into a projection: recognition methods, measurement rules, mappings.

Required: `framework` (e.g. `US_GAAP`, `TAX_US_FED`, `MGMT`), `version`, `applies_when`, `outputs`. Optional: `required_evidence`, `logic_ref` (pointer to executable/testable rule content). Policies MUST be content-versioned: same version ⇒ same logic ⇒ same output for the same inputs.

### 4.9 Relationship
A typed link between records not already expressed by a dedicated field: `duality`, `reciprocal`, `derives_from`, `supports`, `part_of`, `corrects`, `duplicates`, `relates_to`.

Required: `from`, `to`, `type`. Dedicated fields (`settles`, `supersedes`, `agreement`, …) are the normative form where they exist; Relationship covers the rest and MUST NOT be used to duplicate them.

**`duality`** carries REA's exchange pairing (McCarthy 1982, pp. 561–564): it links the two **event** legs of one economic exchange — the increment event (resources flowing to the entity) with its corresponding decrement event (resources flowing from it). Both `from` and `to` MUST reference event records and MUST differ; RECOMMENDED convention: `from` = the increment-side event, `to` = the decrement-side event, from the reporting entity's perspective. Duality complements `settles`/`fulfills`: those route exchange semantics through commitments (extended-REA fulfillment); `duality` is the direct event-to-event pairing for exchanges where both legs are realized events. Duality is OPTIONAL in v0.1 — McCarthy himself documents exchanges where event-level pairing is legitimately absent (matching too tenuous below aggregate level; gains and losses as isolated increments or decrements).

**`reciprocal`** carries the same pairing one level up, at the promise level (extended REA's Commitment–Commitment participation; Geerts & McCarthy 2002): it links the two **commitment** legs of one contracted exchange — the incoming promise (the entity as obligee) with the outgoing promise it is exchanged for (the entity as obligor). A purchase order's delivery obligation and its payment obligation are reciprocal. Both `from` and `to` MUST reference commitment records and MUST differ; RECOMMENDED convention mirrors duality: `from` = the increment-side commitment, `to` = the decrement-side commitment, from the reporting entity's perspective. Reciprocal complements Agreement: the Agreement *bundles* the commitments of a contract (extended REA's Contracting/Scheduling rationale); `reciprocal` *pairs* the specific give-leg with its take-leg. When both legs are later realized, the fulfilling events SHOULD carry the corresponding `duality` pairing. Reciprocal is OPTIONAL in v0.1.

## 5. Referential integrity

A conformant record set has no dangling references, no cyclic `supersedes` chains, and no two `accepted` assertions asserting contradictory values for the same `{record, attribute}` at the same effective time. Validators MUST check all three.

## 6. Time

Three clocks, all RFC 3339 UTC:

- **`occurred_at`** — when the thing happened in the world.
- **`effective_at` / `effective_period`** — when it takes economic effect (service periods, coverage periods, effective-dated corrections). Defaults to `occurred_at` when absent.
- **`recorded_at`** — when the store learned of it. Assigned by the store; monotone per store; never backdated.

This is sufficient to answer both audit questions: *what did we believe as of system time T?* (filter `recorded_at ≤ T`, apply supersession as of T) and *what do we currently believe about effective period P?* (latest accepted assertions whose effective time intersects P).

## 7. Assertion lifecycle and supersession

```
proposed ──accepted──▶ accepted ──superseded by──▶ superseded
    │                                   ▲
    └──rejected──▶ rejected             │ (new assertion, supersedes=old,
                                        │  with its own evidence/basis)
```

- Any agent MAY propose. Who may **accept** is an authorization question for implementations and policies, not this spec — but acceptance MUST be recorded (via `approvals` or an accepting assertion) with actor and time.
- A superseding assertion MUST reference what it supersedes and SHOULD carry equal-or-better evidence or basis.
- Rejected and superseded assertions are never deleted. They are the answer to "what did we believe at the time?"
- Events, commitments, and attribute values inherit their canonical standing from their governing assertions. Nothing else confers truth — not the store, not the model, not the UI.

## 8. Evidence and provenance rules

1. Every `accepted` assertion of kind `observation` SHOULD reference at least one evidence record; implementations MAY require it by policy.
2. Evidence content is stored content-addressed (`sha256`), outside the record store; the hash is the durable identity.
3. Provenance traversal is a conformance requirement: from any projection output, a conformant implementation MUST be able to walk output → policy+version → calculation inputs → events → assertions (with approvers) → evidence. This traversal is the specification's reason to exist.
4. Chain-anchored evidence (`external_locator`) carries its own integrity; snapshotting it content-addressed is RECOMMENDED for durability and offline audit.

## 9. Observations, estimates, judgments

Constitutional principle 13, operationalized. Every assertion declares its epistemic kind:

- **`observation`** — a fact in evidence: a transfer occurred, an invoice was received, a contract was signed.
- **`estimate`** — a measured approximation with a method: fair value at a price source, an accrual from a utilization curve, a par assumption for a redeemable token.
- **`judgment`** — a professional determination among alternatives: useful life, collectibility, impairment, materiality treatment.

`estimate` and `judgment` assertions MUST carry `basis` (method + inputs) and SHOULD carry the evidence for those inputs. Projections MUST record which estimate/judgment assertions they consumed, so that a change in judgment reprojects cleanly and visibly — and so an auditor can distinguish *what was observed* from *what was decided*.

## 10. Projections

A projection is a deterministic function: `(accepted facts, accepted estimates/judgments, policy set @ versions) → outputs` (journal entries, balances, schedules, statements, workpapers).

Requirements: reproducibility (same inputs ⇒ byte-identical outputs), input capture (each output names the records and policy versions it consumed), and explainability (each output supports the §8 traversal). The ledger projection — double-entry journal entries and balances — is the reference projection because it is the universal accounting interface; it is not privileged in the record itself.

v0.1 ships the projection *interface* and one worked reference (prepaid amortization and/or the stablecoin settlement example), not exhaustive GAAP coverage.

## 11. Portability

A conformant implementation MUST export, without loss: all records as openREA JSON/JSONL, all content-addressed evidence keyed by hash, the policy set with versions, and the `openrea_version`. A second conformant implementation importing that export MUST reproduce all projections byte-identically. **Exit is a product requirement.** An implementation that cannot pass export/import round-trip is non-conformant regardless of what else it does.

## 12. Conformance

- **Document conformance:** validates against the JSON Schema; passes referential integrity (§5); respects supersession rules (§7); quantities are string decimals (§3.4).
- **Implementation conformance:** ingests all canonical examples; answers the four fixture queries (open obligations; what-did-we-believe-at-T; why-is-this-number-here traversal; export/import round-trip).
- The `tests/conformance/` fixtures are normative. Becoming a second implementation is intended to be a weekend project; the fixtures are sized to that intent.

## 13. Security posture (summary)

Probabilistic agents **propose**; deterministic systems **authorize**. Agents MUST NOT commit canonical records without passing schema validation, policy/authorization checks, and any human approval those policies require. The full security model (supply chain, trust manifests, capability boundaries) lives in `SECURITY.md`.

## Open questions

Genuinely open — argue with us in the issues:

1. Smallest canonical event schema that stays expressive across industries?
2. Which REA concepts adopt directly vs. simplify for small-business reality?
3. Event vs. versioned attribute assertion — where exactly is the line?
4. Bitemporal representation: are three clocks (§6) sufficient, or does effective-time versioning need first-class ranges on every assertion?
5. Estimate/judgment fields (§9): what carries the basis, range, method, and reviewer without turning into workpaper cosplay?
6. Materiality: modeled where — assertion, policy, or projection?
7. Locked/issued reporting periods under append-only truth: freeze semantics?
8. Policy changes vs. factual corrections: propagation rules through issued periods?
9. Authorization tiers for autonomous-agent acceptance of low-risk assertions?
10. The export format (§11): JSONL + hash-keyed blobs — sufficient, or does it need a manifest/merkle root?
11. Duality and reciprocal (§4.9): should the exchange pairings be promotable from optional relationships to required ones — duality for exchange-classified events, reciprocal for contracted commitments — and how are the legitimate unpaired cases represented (matching too tenuous below aggregate level, gains/losses as isolated legs; McCarthy 1982 pp. 573–575), and unilateral or non-reciprocal commitments?

---

*openREA operationalizes the Resources-Events-Agents ontology (McCarthy, 1982; ISO 15944-4) for agent consumption. See README for prior art and positioning.*
