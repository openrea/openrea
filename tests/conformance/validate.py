#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""openREA document-conformance validator (v0.1-draft).

Checks what JSON Schema alone cannot (SPEC §5, §7) on top of schema validation:
  1. schema validity (schema/openrea.schema.json, draft 2020-12, format-checked)
  2. id uniqueness
  3. referential integrity (no dangling refs; refs point at the right record type
     where the spec makes the type unambiguous)
  4. supersession acyclicity
  5. no contradictory accepted assertions for the same {record, attribute}

Usage:
  validate.py FILE...            validate documents, exit non-zero on failure
  validate.py --suite            run the repo suite: examples/ and valid/ must
                                 pass, invalid/ must fail (each for a reason)
"""
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SCHEMA = json.loads((ROOT / "schema" / "openrea.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

# field -> (path spec, expected record_type or None)
# path spec: dotted; [] marks list traversal.
REF_FIELDS = {
    "agent": [("operated_by", "agent")],
    "resource": [],
    "policy": [],
    "agreement": [("parties[]", "agent"), ("commitments[]", "commitment"), ("evidence[]", "evidence")],
    "evidence": [("describes[]", None)],
    "commitment": [("obligor", "agent"), ("obligee", "agent"), ("agreement", "agreement"),
                   ("terms.resource", "resource")],
    "assertion": [("subject", None), ("subject.record", None), ("asserted_by", "agent"),
                  ("evidence[]", "evidence"), ("supersedes", "assertion"), ("approvals[].agent", "agent")],
    "event": [("participants[].agent", "agent"), ("flows[].resource", "resource"),
              ("flows[].from_agent", "agent"), ("flows[].to_agent", "agent"),
              ("settles[]", "commitment"), ("fulfills[]", "commitment"),
              ("evidence[]", "evidence"), ("subject", None)],
    "relationship": [("from", None), ("to", None)],
}


def walk(value, path):
    """Yield leaf values at a dotted path with [] list markers."""
    if not path:
        if isinstance(value, str):
            yield value
        return
    head, rest = path[0], path[1:]
    if head.endswith("[]"):
        for item in value.get(head[:-2], []) if isinstance(value, dict) else []:
            yield from walk(item, rest)
    else:
        if isinstance(value, dict) and head in value:
            yield from walk(value[head], rest)


def check_document(doc):
    errors = []

    schema_errors = sorted(VALIDATOR.iter_errors(doc), key=lambda e: list(e.absolute_path))
    for e in schema_errors[:10]:
        loc = "/".join(str(p) for p in e.absolute_path) or "(root)"
        errors.append(f"schema: {loc}: {e.message[:140]}")
    if schema_errors:
        return errors  # structural problems make later checks noisy

    records = doc["records"]
    ids, types = {}, {}
    for r in records:
        rid = r["id"]
        if rid in ids:
            errors.append(f"integrity: duplicate id {rid!r}")
        ids[rid] = r
        types[rid] = r["record_type"]

    # referential integrity + type expectations
    for r in records:
        for path_spec, expected in REF_FIELDS[r["record_type"]]:
            parts = path_spec.split(".")
            # subject may be a plain ref or an object; walk() handles both shapes
            for ref in walk(r, parts):
                if ref not in ids:
                    errors.append(f"integrity: {r['id']}: {path_spec} -> dangling ref {ref!r}")
                elif expected and types[ref] != expected:
                    errors.append(
                        f"integrity: {r['id']}: {path_spec} -> {ref!r} is a "
                        f"{types[ref]}, expected {expected}")

    # exchange pairings: duality links two distinct events, reciprocal links
    # two distinct commitments (SPEC §4.9)
    pairings = {"duality": "event", "reciprocal": "commitment"}
    for r in records:
        if r["record_type"] == "relationship" and r.get("type") in pairings:
            expected = pairings[r["type"]]
            if r.get("from") == r.get("to"):
                errors.append(f"integrity: {r['id']}: {r['type']} from and to must differ")
            for end in ("from", "to"):
                ref = r.get(end)
                if ref in types and types[ref] != expected:
                    errors.append(
                        f"integrity: {r['id']}: {r['type']} {end} -> {ref!r} is a "
                        f"{types[ref]}, expected {expected}")

    # supersession acyclicity
    supers = {r["id"]: r["supersedes"] for r in records
              if r["record_type"] == "assertion" and r.get("supersedes")}
    for start in supers:
        seen, cur = set(), start
        while cur in supers:
            if cur in seen:
                errors.append(f"integrity: cyclic supersedes chain involving {start!r}")
                break
            seen.add(cur)
            cur = supers[cur]

    # contradictory accepted assertions on the same {record, attribute}
    accepted = {}
    for r in records:
        if r["record_type"] != "assertion" or r["status"] != "accepted":
            continue
        subj = r["subject"]
        key = (subj["record"], subj["attribute"]) if isinstance(subj, dict) else (subj, None)
        claim = json.dumps(r.get("claim", {}), sort_keys=True)
        if key in accepted and accepted[key][1] != claim:
            errors.append(
                f"integrity: contradictory accepted assertions on {key}: "
                f"{accepted[key][0]!r} vs {r['id']!r} (neither superseded)")
        accepted.setdefault(key, (r["id"], claim))

    return errors


def validate_file(path):
    try:
        doc = json.loads(Path(path).read_text())
    except json.JSONDecodeError as e:
        return [f"parse: {e}"]
    return check_document(doc)


def run_suite():
    failures = 0
    must_pass = sorted((ROOT / "examples").glob("*.json")) + sorted((HERE / "valid").glob("*.json"))
    must_fail = sorted((HERE / "invalid").glob("*.json"))
    for p in must_pass:
        errs = validate_file(p)
        status = "PASS" if not errs else "FAIL"
        print(f"[{status}] expect-valid   {p.relative_to(ROOT)}")
        for e in errs:
            print(f"         {e}")
        failures += bool(errs)
    for p in must_fail:
        errs = validate_file(p)
        status = "PASS" if errs else "FAIL"
        print(f"[{status}] expect-invalid {p.relative_to(ROOT)}"
              + (f"  ({len(errs)} error{'s' if len(errs) != 1 else ''}: {errs[0][:90]})" if errs else "  (validated clean — it should not)"))
        failures += not errs
    print(f"\n{'OK' if not failures else 'FAILED'} — {failures} unexpected result(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--suite"]:
        sys.exit(run_suite())
    if not args:
        print(__doc__)
        sys.exit(2)
    rc = 0
    for f in args:
        errs = validate_file(f)
        print(f"[{'PASS' if not errs else 'FAIL'}] {f}")
        for e in errs:
            print(f"  {e}")
        rc |= bool(errs)
    sys.exit(rc)
