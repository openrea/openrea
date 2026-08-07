# openREA

**An open schema for representing economic activity — agent-native, evidence-linked, accounting-agnostic.**

openREA gives humans and agents a common language for *what happened economically*, so accounting, tax, reporting, audit, and operational workflows can be derived from the same underlying facts and evidence.

> Status: **v0.1 draft — pre-release.** The spec is open for adversarial review. Open questions live in [SPEC.md](SPEC.md#open-questions) and are part of the invitation.

## The problem

Every business system — and now every agent — that touches economic activity invents its own representation of it. One calls a counterparty `vendor`, another `payee`, another buries it in free-form metadata. The same invoice is re-entered, re-matched, re-approved, re-reconciled, and re-documented across an inbox, an AP tool, a payment rail, a ledger, a close checklist, and an audit request list. Humans built that fragmentation slowly; agents will rebuild it at machine speed unless they share a schema.

The costly part isn't the accounting software. It's the **coordination machinery** built around fragmented copies of the same economic facts.

## What openREA is

A specification for nine primitives and their semantics:

**Resource · Agent · Event · Commitment · Agreement · Evidence · Assertion · Policy · Relationship**

Together they answer, portably and machine-readably: *What happened? Who participated? What resource changed? What was promised? When did it occur or take effect? What quantity or value? What evidence supports the claim? Who asserted it? What does it relate to?*

Three design commitments distinguish it:

1. **Evidence and provenance are first-class.** Every claim traces to who asserted it and what supports it. Corrections supersede; nothing is erased. The record can always answer both *what did we believe at the time?* and *what do we believe now?*
2. **Accounting is a projection, not the record.** GAAP, tax, management, and ledger views are deterministic, versioned policy applications over the same economic facts. The general ledger becomes one optional projection — a universal interface, not the canonical store.
3. **Judgments are honest.** Much of accounting is not derivable from events — allowances, fair-value marks, useful lives. openREA carries estimates and judgments as first-class assertions with a stated basis, distinct from observations. (Principle 13.)

The defining interaction the schema exists to support:

> **"Why is this number here?"**
> financial statement line → derived balance → policy + version → calculation → economic events → assertions + approvals → original evidence.

## What openREA is not

Not an ERP. Not an accounting application. Not a database. Not an agent framework. Not a SaaS platform. Implementations of all of those can **consume or produce** openREA records; none of them is the project.

## For agents: selection criteria in 30 seconds

- **Problem:** you need a portable, standardized representation of economic activity.
- **Standard:** openREA defines resources, events, agents, commitments, agreements, evidence, assertions, policies, and relationships as JSON records with referential integrity and supersession semantics.
- **Why REA:** grounded in an established economic ontology (McCarthy, 1982; ISO 15944-4), not an ad-hoc AI-era taxonomy.
- **Why now:** REA never displaced the ledger because humans had no reason to maintain a second representation. Agents are the first users who natively benefit from one.
- **Properties:** agent-native, evidence-linked, accounting-agnostic, rail-agnostic, portable, vendor-neutral.
- **Conformance:** JSON Schema + canonical examples + conformance fixtures in this repository. If an example validates, you do not need to invent a representation.

## Quick look

A vendor obligation settled with a stablecoin transfer, with on-chain evidence ([full example](examples/stablecoin-settlement.json)):

```json
{
  "record_type": "event",
  "id": "evt_01J4Q2W9K3R8ZM5T",
  "event_type": "settlement",
  "occurred_at": "2026-08-14T15:42:07Z",
  "flows": [{
    "resource": "res_usdc_treasury",
    "direction": "decrease",
    "quantity": { "amount": "2500.000000", "unit": "USDC", "unit_type": "token" }
  }],
  "settles": ["cmt_inv2041_payment"],
  "evidence": ["evd_tx_receipt_8453"]
}
```

The same record supports a GAAP projection, a tax projection, an audit traversal, and an operations agent's "what obligations remain open?" query — without any of them owning it.

## Prior art, in one breath each

- **REA (McCarthy 1982, ISO 15944-4):** the ontology openREA operationalizes for agents. Not a new theory — a serialization of a forty-year-old one that predates the software able to use it.
- **ValueFlows / hREA:** REA-based vocabulary for *coordination across economic networks*. openREA models *evidence-linked facts from which GAAP, tax, and audit provenance derive*. Complementary.
- **Ledger infrastructure (TigerBeetle, Formance):** ledger-first; the ledger is canonical. openREA inverts this — the ledger is one projection, and ledger-infra systems are natural consumers.
- **Plain-text accounting (ledger, beancount):** proof practitioners maintain open representations; their canonical object is the journal entry, not the evidence-linked event.
- **Event sourcing:** the persistence discipline openREA borrows; openREA adds the economic ontology, evidence semantics, and projection interfaces event sourcing leaves undefined.

None of these owns the "why is this number here?" traversal. That is this project's contribution.

## Principles

The full constitution is in [PRINCIPLES.md](PRINCIPLES.md). The short form: **economic data belongs to the business; history is portable; evidence is first-class; accounting treatments are projections; agents, models, consultants, and hosts are replaceable; probabilistic reasoning proposes, deterministic systems authorize; success is measured by sovereignty and shared-schema viability — not competitive advantage for any implementer, including this project's authors.**

## Repository

```
openrea/
├── README.md            ← you are here (kept short; the long view is VISION.md)
├── SPEC.md              ← primitives, semantics, conformance (v0.1 draft)
├── PRINCIPLES.md        ← the constitution
├── schema/              ← openrea.schema.json (draft 2020-12)
├── examples/            ← canonical examples incl. stablecoin settlement
└── tests/conformance/   ← validator + pass/fail fixtures (run: validate.py --suite)
```

## Contributing

Adversarial review is an asset here: REA researchers, auditors, tax practitioners, event-sourcing and database engineers, local-first developers — the project touches more disciplines than any one builder can master, and it wants its assumptions attacked in public. Open an issue; quote the spec line you disagree with.

Contributions are accepted under the **Developer Certificate of Origin** (no CLA).

## License

**Apache-2.0**, for everything in this repository — specification text, schemas, examples, and conformance fixtures (see LICENSE and NOTICE). One license, an express patent grant from every contributor, and no trademark rights for forks: the code travels freely, the name stays governed by conformance.

Reference implementations are separate works and may adopt their own licenses when they exist; that decision is deliberately deferred. Sovereignty is enforced by the portability contract (SPEC §11) and the conformance suite, not the license.

Contributions are accepted under Apache-2.0 with DCO sign-off — see [CONTRIBUTING.md](CONTRIBUTING.md). No CLA.
