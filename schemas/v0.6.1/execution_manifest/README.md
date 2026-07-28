# CASEF v0.6.1 execution-manifest schema

## Authority and scope

`execution_manifest.schema.json` is the development-stage Draft 2020-12 structural schema for one complete canonical CASEF `execution_manifest` record. It implements the planned-execution contract in [`spec/execution_manifest_contract.md`](../../../spec/execution_manifest_contract.md) under the ownership, gate, and serialization authorities of the repository.

The schema does not create a manifest instance, authorize an execution, establish referent existence or hash agreement, create evidence eligibility, execute a test, or authorize qualification or use.

## Files

- `execution_manifest.schema.json` — complete closed record schema;
- `tests/execution_manifest_cases.json` — machine-readable expected-valid and expected-invalid structural vectors.

The vectors are structural test data. They are not canonical manifest instances, execution authorization, or evidence.

## Root and composition behavior

The root validates a complete `execution_manifest` object and closes its final boundary with `unevaluatedProperties: false`.

The schema composes and closes:

- selected canonical `test_spec` record references;
- non-record Context-of-Use references;
- human-or-tool preparer identities; and
- human-only authorizer identities.

`record_id` in a selected-test reference carries the canonical `test_id`. No separate duplicate `test_id` is added. Context of Use remains a versioned non-record contract input.

## Planned structures

The schema contains planned facts only: target, interface, execution conditions, generation settings, tool conditions, session conditions, slots, and capture, validation, and rating requirements. It does not admit observed targets, actual execution timestamps, execution or capture status, captured artifacts, findings, severity, qualification outcomes, or policy consequences.

Selected tests, conditions, settings, tools, slots, and requirement arrays are `SET_LIKE_COLLECTION` values. JSON Schema rejects exact duplicate items; semantic identity uniqueness and owner-defined stable-key ordering remain content-aware responsibilities.

Validation and rater requirements bind upstream test requirement IDs to planned run slots. Validator references, validator logic, rater-protocol references, and required-rater counts remain owned by the exact selected `test_spec` and rater protocol.

## Lifecycle conditionals

- `DRAFT` prohibits authorization fields.
- `AUTHORIZED` requires both authorization fields and at least one capture requirement.
- `SUPERSEDED` and `CANCELLED` require a predecessor version and reason.
- A terminal lifecycle version permits either both authorization fields or neither. Cross-record validation must establish whether the predecessor lineage was authorized and whether provenance was preserved.
- Supersession and authorization optional fields use absence, not null.

Lifecycle changes are additive manifest versions. They do not rewrite an immutable authorized version. A never-authorized plan may receive a `CANCELLED` lifecycle version without authorization provenance.

## Structural and content-aware boundary

The schema enforces object shape, closure, enums, lexical references and hashes, conditional requiredness, null-versus-absence rules, basic cardinality, and human-only authorization identity.

Content-aware validation must separately establish:

- referent existence and content-hash agreement;
- selected-test `FROZEN` and `ELIGIBLE` status;
- suite composition;
- slot-to-test agreement and semantic identity uniqueness;
- complete capture, validation, and rating coverage;
- Context-of-Use compatibility;
- actual authorizer authority and timestamp ordering;
- same-lineage supersession and immutable-plan preservation;
- prevention of diagnostic promotion and slot reuse.

Schema success does not prove any of these facts.

## Local validation

From the repository root:

```text
python tools/validate_schemas.py
python -m unittest discover -s tests -p "test_schema_validation.py"
```

The committed harness discovers this schema and its vectors dynamically through the local no-network schema registry.

## Current non-capabilities

No canonical manifest instance, runner, model or API execution, source-artifact capture, hashing implementation, cross-record validator, rater execution, gate execution, evidence generation, qualification, or use permission is created here.
