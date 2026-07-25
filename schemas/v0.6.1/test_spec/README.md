# CASEF v0.6.1 executable test-specification schema

## Authority and scope

[`test_spec.schema.json`](test_spec.schema.json) is the first complete executable canonical-record schema in CASEF. It implements the structural and lifecycle requirements owned by [`spec/test_spec_contract.md`](../../../spec/test_spec_contract.md) under the evidence, gate, and serialization authorities identified there.

The schema owns no execution observation, finding, severity, qualification outcome, policy consequence, or gate authority.

## Files

- `test_spec.schema.json` is the complete Draft 2020-12 structural schema for one `test_spec` record.
- `tests/test_spec_cases.json` contains seven expected-valid and 32 expected-invalid structural vectors.

The vectors are structural test data. They are not approved or canonical test-specification instances and do not migrate the current Markdown test assets.

## Full-record behavior

Unlike the common definition-container roots, the `test_spec` root validates a complete record and closes it with `unevaluatedProperties: false`. Unknown top-level properties fail.

Nested prompt, output, criterion, assessment-requirement, and applicability structures are closed. Validator and rater-protocol references compose the common versioned-contract base and close only after their owner-specific identifiers and versions are declared. `approved_by` composes the common human-actor base and rejects tool actors and direct personal-name or contact keys.

## Lifecycle conditionals

- `DRAFT` requires `NOT_ELIGIBLE`, prohibits approval provenance, and may omit authored prompt, output, and acceptance content.
- `FROZEN` requires complete authored content, human approval provenance, and at least one deterministic or human assessment requirement.
- `RETIRED` retains the same approved content and provenance as `FROZEN` and requires `NOT_ELIGIBLE`.
- `ELIGIBLE` is permitted only for `FROZEN`.
- For an `ELIGIBLE` record, the schema requires each assessment family indicated by the declared `assessment_method` values: `DETERMINISTIC` and `BOTH` require deterministic assessment requirements, while `HUMAN` and `BOTH` require human assessment requirements.
- Supersession version and reason must appear together.

Exact referential coverage—whether every `criterion_id` is linked to the correct specific requirement—requires content-aware validation outside this structural schema. Schema success does not prove scientific validity or assessment completeness beyond the structural checks stated here, and these conditions do not create evidence eligibility, qualification, or use permission.

## Composition dependencies

The schema resolves relative `$ref` values to:

- `../common/scalars.schema.json`;
- `../common/references.schema.json`; and
- `../common/actors.schema.json`.

Local development validation uses the committed harness's explicit immutable-`$id` registry and does not retrieve schemas from the network.

## Local validation

Install only the bounded development requirements, then run:

```text
python -m pip install -r requirements-schema-validation.txt
python tools/validate_schemas.py
python -m unittest discover -s tests -p "test_schema_validation.py"
```

## CI and non-capabilities

The `Schema Validation` GitHub Actions workflow runs the harness and its standard-library unit tests on pushes and pull requests. It performs structural development checks only.

This tranche adds no runner, model or API call, prompt capture, record or artifact hashing, RFC 8785 implementation, canonical record instance, evidence generation, gate execution, qualification, production CLI, SDK, or UI.
