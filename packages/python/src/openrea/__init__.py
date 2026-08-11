# SPDX-License-Identifier: Apache-2.0
"""openREA — schema-only convenience package.

Exposes the openREA JSON Schema (draft 2020-12) for validating
`.openrea.json` documents. The canonical schema and specification live at
https://github.com/openrea/openrea — this package is a thin distribution
vehicle so tooling and agents can `pip install openrea-schema` (imports as `openrea`) and validate.

    import openrea
    openrea.SCHEMA          # the schema as a dict
    openrea.SCHEMA_VERSION  # "0.1-draft"
    openrea.validate(doc)   # requires the [validate] extra (jsonschema)

Note: full conformance requires the cross-record checks (referential
integrity, supersession acyclicity, contradiction detection) implemented in
the repository's tests/conformance/validate.py; JSON Schema alone is level-1
document validity's first layer.
"""
import json
from importlib.resources import files

__all__ = ["SCHEMA", "SCHEMA_VERSION", "schema_json", "validate"]

SCHEMA = json.loads(files(__package__).joinpath("openrea.schema.json").read_text(encoding="utf-8"))
SCHEMA_VERSION = SCHEMA["properties"]["openrea_version"]["const"]


def schema_json() -> str:
    """The schema as a JSON string."""
    return json.dumps(SCHEMA, indent=2)


def validate(document: dict) -> None:
    """Validate a document against the openREA schema.

    Raises jsonschema.ValidationError on failure. Requires the
    ``openrea[validate]`` extra.
    """
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "schema validation requires the 'validate' extra: pip install 'openrea-schema[validate]'"
        ) from exc
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(document)
