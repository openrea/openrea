# openrea

The [openREA](https://github.com/openrea/openrea) JSON Schema as an installable package — an open, agent-native, evidence-linked representation of economic activity, from which accounting, tax, and audit views derive.

```python
import openrea

openrea.SCHEMA           # the JSON Schema (draft 2020-12) as a dict
openrea.SCHEMA_VERSION   # "0.1-draft"
openrea.validate(doc)    # pip install 'openrea-schema[validate]'
```

Documents use the `.openrea.json` suffix. This package is schema-only by design: the specification, canonical examples, conformance suite, and open questions live in the repository. Full document conformance additionally requires the cross-record checks (referential integrity, supersession acyclicity, contradiction detection) that JSON Schema cannot express — see [`tests/conformance`](https://github.com/openrea/openrea/tree/main/tests/conformance).

Apache-2.0. The spec is a v0.1 draft and is built to be attacked: [issues](https://github.com/openrea/openrea/issues).
