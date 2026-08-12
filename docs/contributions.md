# What openREA Adds — Contributions and Debts (non-normative)

Status: honest inventory, maintained alongside the v0.1 draft. Serious evaluators ask "what's actually new here?" — this document answers it with attribution, so the claim can be checked rather than taken on tone. Corrections welcome as issues.

## The one-sentence version

**The REA lineage modeled the economy; openREA models the economy plus the accountability of the record itself** — who asserted what, on what evidence, under which versioned policy, checkable by machine. openREA does not extend REA's economics; it builds the lineage's assurance layer — the application McCarthy's own final paragraph named as unexplored in 1982 ("internal control specification and audit evidence gathering").

## Inherited — the debts, stated plainly

On the economic ontology, openREA invents almost nothing:

| Element | Source |
|---|---|
| Events-not-debits; resources; agents; accounting artifacts as derivations; balances and claims as derived imbalances; multiple views over one record | McCarthy 1982 |
| Duality (event↔event exchange pairing) | McCarthy 1982, pp. 561–564 |
| Commitments, agreements, `executes`→`fulfills`, reciprocity, reserves | Geerts & McCarthy 2000 (answering McCarthy 1982 p. 576) |
| The exchange-completeness axioms (openREA open question 11) | Geerts & McCarthy 2000 |
| Binary accountability (ternary control → per-participant links) | Geerts & McCarthy 2002 |
| The "what is" vs "what should/could/must be" split; policy kinds (knowledge-intensive, validation, target) | Geerts & McCarthy 2002, 2006 |
| Append-only instinct ("maximum temporal generality"); derivation-procedure taxonomy | McCarthy 1982 |
| Claims derivable by predicate over the event graph | Geerts & McCarthy's CREASY (1999/2000) |

The spec's commit history cites these to page numbers where changes were made because of them.

## Contributed — five things not in any of the referenced work

1. **Evidence as a typed primitive with cryptographic identity.** Supporting artifacts are records: content-addressed by hash, or anchored to external systems of integrity (e.g. on-chain transactions), attached to events and assertions. The lineage never built its named future-work item; ValueFlows' "provenance" is resource lineage through flows, not documentary support. (SPEC §4.6, §8.)
2. **The assertion layer — epistemics of the record.** Nothing in the lineage models *who claims a fact*, with what confidence, approved by whom, superseded when — and nothing distinguishes **observation from estimate from judgment**, with a mandatory stated basis for the latter two. The record models knowledge about the economy, not just the economy; bitemporality ("what did we believe at time T?") follows. (SPEC §4.7, §6, §7, §9; principle 13.)
3. **Autonomous agents as accountable participants.** `autonomous_agent` is a first-class agent kind with a mandatory operating principal; agents observe and propose, deterministic systems authorize, obligations bind principals. The lineage discussed agents communicating *via* ontologies (KQML, 2000); it did not place them *inside* the economy with a liability chain. (SPEC §4.2, §13.)
4. **Projection as an engineering contract.** The lineage gestures at derivability throughout — 1982's procedure types, 2006's policy kinds, ValueFlows' "a computer program on request." openREA specifies the discipline: content-versioned deterministic policies, same-inputs ⇒ byte-identical outputs, input capture, framework scoping (GAAP/tax/management as parallel projections), and the **"why is this number here?" traversal as a conformance requirement**. CREASY demonstrated derivation; openREA contracts it. (SPEC §4.8, §10, §8.3.)
5. **Conformance and portability as normative machinery.** Executable pass/fail fixtures, typed referential-integrity checks, supersession acyclicity, the export/import round-trip as a requirement ("exit is a product requirement"), and an independent second implementer as the stated success metric. The academic lineage had no conformance story; ValueFlows is a vocabulary without one. (SPEC §5, §11, §12; tests/conformance.)

Secondary but real: a JSON-native serialization with practitioner invariants — string-decimal amounts (never floats), congruent multi-flow events, typed pairing checks — where the lineage had E-R/UML diagrams and ValueFlows has RDF.

## Subtracted — deliberate drops, each with a stated position

| Dropped | Where the position lives |
|---|---|
| The type layer (type images, typification, characterization) → classification strings + `Policy.applies_when` | Open question 12, with the intensional-subjects candidate resolution |
| Process as a first-class transformation container | Acknowledged gap (ValueFlows mapping, Seam table) |
| The coordination layer (intents, proposals, offers/matching) | Out of scope by design; ValueFlows specifies it richly |
| Rich flow verbs (five stock-flow verbs, 2000; nineteen actions incl. rights/custody, VF) | Candidate `flow_kind`; rights/custody flagged with digital-asset motivation |
| Materialized claims | openREA derives claims from un-dualized flows — the other end of McCarthy 1982's own compromise spectrum from ValueFlows' materialized `Claim` |

## Calibration — what "novel" means here

Novel **within the REA/accounting lineage**. Adjacent bodies of work exist and are positioned, not ignored: event sourcing supplies the persistence discipline (README, prior art); ledger infrastructure and plain-text accounting are adjacencies with the journal as their canonical object; **W3C PROV** models attribution of assertions in the linked-data world and is the strongest "this exists elsewhere" citation — it does not do economics, evidence-as-audit-support, or accounting projection, and a positioning note against it belongs in a future revision of this document.

The contribution is not any single atom. It is the synthesis: economic ontology, evidential epistemics, policy-as-code, and executable conformance in one small schema — a combination that seems to have required a practitioner standing in all four rooms at once.
