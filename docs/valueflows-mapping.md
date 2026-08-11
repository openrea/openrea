# openREA ↔ ValueFlows 1.0 — Mapping (non-normative draft)

Status: **draft for adversarial review**, written against ValueFlows 1.0 ("major stable release," [valueflo.ws](https://www.valueflo.ws/)) and openREA v0.1-draft. This document is non-normative: it claims a mapping so the claim can be attacked. Errors are the author's; the issues tab is open.

## The relationship, stated plainly

Both vocabularies descend from REA and both hold that **the ledger is a projection** — ValueFlows: statements "can be created by a computer program on request"; openREA: SPEC §10. The difference is which half of the problem each specifies:

- **ValueFlows is coordination-rich, assurance-thin.** It richly specifies the layers *before and around* economic facts — proposal → intent → commitment → event, processes and recipes, nineteen typed actions — and leaves the projection discipline unspecified.
- **openREA is assurance-rich, coordination-thin.** It specifies evidence and provenance as first-class, assertion epistemics (observation/estimate/judgment), versioned deterministic policies, and conformance/portability contracts — and deliberately specifies nothing about offers, matching, or planning.

The composability thesis: **a VF network's observation layer and an openREA record set can describe the same economic activity without fighting**, so a business could coordinate in VF and carry assurance in openREA. The tables below are that thesis made checkable.

Fidelity legend: **CLEAN** (direct, lossless with a stated rule) · **PARTIAL** (mappable with loss or convention) · **NONE** (no counterpart; deliberate scope difference unless marked as a gap).

## Class mapping

| ValueFlows | openREA | Fidelity | Notes |
|---|---|---|---|
| Agent | `agent` | CLEAN− | VF: person/organization/*ecological* agents. openREA: person/organization/system/**autonomous_agent** (+ mandatory `operated_by`). Each has a kind the other lacks; both map through `kind` + `metadata`. |
| EconomicResource | `resource` | CLEAN− | `resourceInventoriedAs` ≈ flow→resource ref. VF ResourceSpecification (knowledge level) lands on openREA's `kind` string — see Q12. |
| EconomicEvent | `event` | **PARTIAL, with a granularity rule** | See "Seam 1" below. VF's unit is one action on one resource; an openREA event may carry multiple flows. Rule: VF event ↔ openREA event with exactly one flow; an openREA multi-flow (congruent) event ↔ a set of VF events sharing an agreement/`metadata` bundle. |
| Process | — | **NONE (openREA gap)** | openREA has no transformation container; `event_type` + flows carry conversions without a process identity. VF is ahead here, as extended REA's transformation duality suggests it should be. |
| Commitment | `commitment` | CLEAN | provider/receiver ↔ obligor/obligee; action+resourceQuantity ↔ `terms`; `fulfills` ↔ `fulfills`. |
| Intent | — | NONE (scope) | Pre-obligation desiderata are coordination; openREA starts at the promise. |
| Proposal | — | NONE (scope) | Offers/requests and matching are coordination. |
| Agreement | `agreement` | CLEAN, with a rule | `stipulates`/`stipulatesReciprocal` ↔ `agreement.commitments[]` **plus** a `reciprocal` relationship between the paired commitments (SPEC §4.9). |
| Claim | *(derived)* | **PARTIAL — the spectrum** | See "Seam 3." VF materializes claims (`triggeredBy`/`settles`); openREA derives them from un-dualized flows and open commitments. Both are points McCarthy named on the same compromise spectrum in 1982. |
| Plan / Scenario | — | NONE (scope) | Coordination. |
| ResourceSpecification / ProcessSpecification / recipes | — | NONE → Q12 | openREA deliberately flattens the knowledge level to classification strings + `Policy.applies_when`; open question 12 (intensional subjects) is the live debate about whether that holds. |
| — | `evidence` | **NONE (VF gap)** | VF's "provenance" is resource lineage through flows — not documentary evidence. Content-addressed / chain-anchored support for claims has no VF counterpart. |
| — | `assertion` | **NONE (VF gap)** | No asserter, confidence, basis, approvals, supersession chains, or bitemporality in VF; events are simply recorded. |
| — | `policy` | **NONE (VF gap)** | "A computer program on request" is exactly the thing openREA specifies: versioned, deterministic, framework-scoped, reproducible. |

## Action mapping (VF's 19 verbs → openREA)

| VF action | openREA rendering | Fidelity |
|---|---|---|
| produce | flow `increase` (event_type: production) | CLEAN |
| consume | flow `decrease` in a transformation event | CLEAN |
| transfer | flow `transfer` + `from_agent`/`to_agent` | CLEAN |
| transferAllRights / transferCustody | **no first-class home** — `metadata` today | **PARTIAL — VF is ahead.** The rights-vs-custody split is exactly what digital-asset accounting needs (custody without rights; rights without custody). Adopting a rights/custody dimension on openREA flows is an open candidate. |
| use / cite / work / accept / modify | event with `subject` (no quantity flow) + `event_type` | PARTIAL — expressible, untyped |
| combine / separate | events + `part_of` relationships | PARTIAL |
| pickup / dropoff / move | `metadata` (openREA has no location model) | PARTIAL (scope) |
| deliverService | flow `increase` of a service-kind resource | PARTIAL |
| copy | flow `increase` without a paired decrease | PARTIAL |
| raise / lower | correction: superseding assertions on the affected records | PARTIAL — VF corrects quantities with verbs; openREA corrects beliefs with assertions. Different philosophies, same books. |

## Mechanism mapping

| VF | openREA | Notes |
|---|---|---|
| `fulfills` (event→commitment) | `fulfills` (event→commitment) | Same name, same direction. |
| `satisfies` (→intent) | — | No intents. |
| `triggeredBy` / `settles` (claims) | derived claims; `settles` (event→commitment) | VF settles claims; openREA settles commitments; the un-dualized remainder *is* the claim (Q11). |
| `corrects` (event→event) | `relationship{type: corrects}` + assertion supersession | openREA has the same edge, plus the epistemic layer under it. |
| `stipulates` / `stipulatesReciprocal` | `commitments[]` + `reciprocal` relationship | Rule stated above. |
| provider / receiver | `flows[].from_agent` / `to_agent` (+ `participants` roles) | CLEAN. |
| `resourceConformsTo` | `kind` string | Q12 territory. |
| `realizes` (agreement→events) | transitive: agreement → commitments → fulfilling events | No direct edge; derivable. |

## The four seams, examined

**Seam 1 — event granularity.** VF: one event = one action on one resource. openREA: one event may carry several flows — deliberately, because extended REA's *congruent exchange* (a cash sale: give and take coinciding in time and space) is one economic occurrence, and openREA models it as one event. The mapping rule (one VF event per openREA flow) is lossless in one direction and requires bundling in the other. **Question for VF:** is there an idiomatic VF way to mark several events as one congruent occurrence, beyond sharing an Agreement?

**Seam 2 — rights vs custody.** VF's transfer triad is finer than anything in the Geerts–McCarthy papers and finer than openREA's single `transfer` direction. openREA's `custody` object on Resource describes *state*, not *flow semantics*. This is the one place the mapping runs uphill against openREA, and the candidate fix (a rights/custody dimension on flows) is noted in the openREA backlog — with digital-asset custody as the motivating case.

**Seam 3 — claims: materialize vs derive.** VF records a Claim when an event implies a reciprocal expectation, then settles it. openREA holds that the un-dualized flow *is* the claim, derivable on demand (McCarthy 1982's imbalances; CREASY's predicate, 1999; openREA Q11). Import rule: a VF Claim entering openREA becomes either a derived query result (preferred) or, where persistence is required, a commitment triggered by the referenced event (lossy: claims arise without prior agreement; commitments imply one). Export rule: openREA's derived claims can be materialized as VF Claims at any time — that direction is easy. Neither position is wrong; McCarthy called the trade in 1982.

**Seam 4 — corrections vs supersession.** VF `corrects` replaces an event's content; openREA supersedes *assertions about* the event, preserving what-was-believed-when. VF's edge maps into openREA losslessly (a `corrects` relationship plus a superseding assertion); openREA's bitemporal answer ("what did we believe on March 3?") does not survive the trip back. For audit purposes that asymmetry is the point.

## A worked crossing

The same USDC settlement (openREA's canonical stablecoin example), in both vocabularies:

**ValueFlows (sketch):**
```
EconomicEvent:
  action: transfer
  provider: Harborlight Advisory LLC
  receiver: Meridian Data Systems Inc.
  resourceQuantity: 2500.000000 USDC
  resourceInventoriedAs: usdc-treasury-holding
  fulfills: payment-commitment-inv2041
```

**openREA (from `examples/stablecoin-settlement.openrea.json`):**
```
event evt_inv2041_settlement:
  event_type: settlement
  flows: [{ resource: res_usdc_treasury, direction: decrease,
            quantity: 2500.000000 USDC,
            from_agent: agt_harborlight, to_agent: agt_meridian }]
  settles: [cmt_inv2041_payment]
  evidence: [evd_tx_receipt_8453]        ← no VF counterpart
+ assertions (observed by an autonomous agent, accepted by a human,
  par-value measurement carried as an estimate with a basis)
                                          ← no VF counterpart
```

The economic fact crosses cleanly. What doesn't cross is everything below the fact — the evidence, the asserter, the approval, the measurement basis. That is the division of labor working as designed.

## Open questions for the ValueFlows community

1. Congruent occurrences: idiomatic VF for bundling the two legs of a simultaneous exchange (Seam 1)?
2. Would VF consider an optional documentary-evidence property (content-addressed artifact refs on EconomicEvent), or is that properly an extension vocabulary — perhaps this one?
3. Is the claims materialize/derive split (Seam 3) worth a shared statement, since both lineages implement opposite ends of McCarthy's 1982 spectrum?
4. For rights/custody (Seam 2): would a joint definition of the transfer triad's semantics serve both projects better than parallel ones?

---

*Non-normative. openREA is Apache-2.0; ValueFlows is its own project under its own terms — nothing here speaks for it. Corrections welcome as issues or PRs against this file.*
