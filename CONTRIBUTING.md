# Contributing to openREA

Adversarial review is the point. The project touches accounting ontology, audit methodology, event sourcing, tax, security, and agent architecture — more disciplines than any one builder can master, so the assumptions want to be attacked in public.

## How to contribute

- **Open an issue and quote the spec line you disagree with.** "SPEC §4.4 derived-status breaks under X" is a perfect issue title. Design arguments beat drive-by opinions; failing fixtures beat both.
- **Pull requests** should keep the conformance suite green (`.venv/bin/python tests/conformance/validate.py --suite`) or change the fixtures *and* the spec together, with the reasoning in the PR body.
- **New canonical examples** are highly valued — especially ones that break the schema. An example the schema can't express honestly is a spec bug.
- The open questions in SPEC.md are live invitations, not rhetorical.

## Licensing of contributions

This repository is licensed under **Apache-2.0** (see LICENSE). Contributions are accepted under the same license — inbound equals outbound. There is no CLA and there will not be one.

## Developer Certificate of Origin

All commits must be signed off (`git commit -s`), certifying the Developer Certificate of Origin 1.1 (developercertificate.org):

```
By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I have
    the right to submit it under the open source license indicated in
    the file; or
(b) The contribution is based upon previous work that, to the best of
    my knowledge, is covered under an appropriate open source license
    and I have the right under that license to submit that work with
    modifications, whether created in whole or in part by me, under
    the same open source license (unless I am permitted to submit
    under a different license), as indicated in the file; or
(c) The contribution was provided directly to me by some other person
    who certified (a), (b) or (c) and I have not modified it.
(d) I understand and agree that this project and the contribution are
    public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

Sign-off is a statement of provenance — fitting, for this project in particular.
