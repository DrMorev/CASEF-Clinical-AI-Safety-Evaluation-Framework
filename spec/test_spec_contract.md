# CASEF v0.6.1 canonical test-specification contract

## 1. Purpose and authority

This document governs the documentation-level field and invariant contract for canonical `test_spec` records in CASEF v0.6.1.

`docs/canonical_evidence_contract.md` remains authoritative for record ownership and evidence-chain boundaries. `docs/gates.md` remains the sole authority for qualification and gate semantics. This contract is subordinate to both documents within their respective authority.

This contract does not define JSON Schema, qualification outcomes, policy consequences, or active gate rules. It does not make a test executable by itself.

## 2. Record ownership boundary

A canonical `test_spec` owns:

- stable test identity;
- the exact test version;
- the tested construct and construct version;
- the exact prompt or stimulus protocol;
- the expected output contract;
- acceptance criteria;
- separate deterministic and human assessment requirements;
- execution eligibility;
- applicability boundaries; and
- prohibited interpretations.

A `test_spec` must not own:

- suite membership or suite version;
- a planned execution target or execution plan;
- actual execution observations or timestamps;
- captured model output;
- validator execution results or deterministic findings;
- human findings;
- final severity;
- qualification outcomes; or
- policy consequences.

Those facts belong to the other canonical records identified by `docs/canonical_evidence_contract.md`.

## 3. Field dictionary

| Field | Requirement | Meaning and constraints |
|---|---|---|
| `schema_version` | Required | Exact supported version of this documentation-level contract; distinct from `test_version` and `construct_version` |
| `test_id` | Required, non-null | Stable identity for one test construct; filenames are not authoritative identity |
| `test_version` | Required, non-null | Exact version of the test contract; it becomes immutable on approval, and an incomplete pre-canonical artifact is not made canonical by assigning placeholder values |
| `title` | Required | Human-readable title that does not redefine `test_id` or the construct |
| `level` | Required | CASEF test-level classification; it is not harm severity or a qualification result |
| `construct_id` | Required | Stable identity of the behavior or property being measured |
| `construct_version` | Required | Exact version of the construct definition used by this test version |
| `purpose` | Required | Bounded statement of what the test is intended to establish |
| `prompt_protocol` | Required for an approved test | Exact closed, versioned prompt or stimulus protocol, including ordering and registered variants where applicable |
| `expected_output_contract` | Required for an approved test | Exact structural or behavioral output expectations used by the assessment requirements |
| `acceptance_criteria` | Required for an approved test | Test-level criteria stated independently of qualification outcomes and policy consequences |
| `deterministic_assessment_requirements` | Required collection | Exact deterministic assessment requirements and referenced validator identity where applicable; empty only when deterministic assessment is not required |
| `human_assessment_requirements` | Required collection | Exact human-assessment and versioned protocol requirements where applicable; empty only when human assessment is not required |
| `execution_eligibility` | Required | Exactly `ELIGIBLE` or `NOT_ELIGIBLE`; separate from `spec_status` |
| `applicability` | Required | Conditions and boundaries under which the test contract is scientifically and operationally applicable |
| `prohibited_interpretations` | Required collection | Claims or inferences that the test does not support, including conclusions broader than its construct and evidence |
| `spec_status` | Required | Exactly `DRAFT`, `FROZEN`, or `RETIRED` |
| `created_timestamp_utc` | Required | Canonical UTC timestamp for creation of the specification version |
| `approved_timestamp_utc` | Required for `FROZEN` or `RETIRED` | Canonical UTC timestamp of approval; for an unapproved `DRAFT`, the field must be absent and null is prohibited |
| `approved_by` | Required for `FROZEN` or `RETIRED` | Identity and approval role for the exact version; for an unapproved `DRAFT`, the field must be absent and null is prohibited |
| `supersedes_test_version` | Optional | Earlier version of the same `test_id` superseded by this version; when no predecessor exists, the field must be absent and null is prohibited |
| `supersession_reason` | Conditionally required | Bounded reason for supersession; required when `supersedes_test_version` is present; otherwise, the field must be absent and null is prohibited |

Canonical serialization and timestamp syntax are governed by `docs/canonical_serialization_contract.md` and implemented by the reviewed executable schemas. Canonical `test_spec` serialization uses field absence for these non-applicable optional states. Null and sentinel strings such as `"NONE"`, `"N/A"`, or `"UNKNOWN"` are prohibited substitutes.

## 4. Stable identity and versioning invariants

1. One `test_id` identifies one stable test construct.
2. A change that preserves the construct but changes the approved prompt protocol, expected output contract, acceptance criteria, or assessment requirements creates a new `test_version`.
3. A material change to the measured construct creates a new `test_id`; an old ID must not be silently reinterpreted.
4. An approved test version is immutable. Corrections or compatible clarifications after approval create a new version with explicit supersession.
5. A filename, heading, registry entry, or suite selection may reference test identity but cannot redefine it.
6. One test version contains one closed, versioned prompt protocol. It may be one prompt, an ordered multi-turn sequence, a fixed A/B pair, or a closed variant set required by the construct. Unregistered or freely substitutable prompt variants are prohibited.

The deleted non-canonical demo artifacts do not create an alias, alternate meaning, or migration obligation for `TC-L1-JSON-01`. Its active identity remains the specification at `spec/tests/level1/TC-L1-JSON-01.md`. That existing asset is not migrated or modified by this contract patch.

## 5. Specification status

The `spec_status` vocabulary is exactly:

| Value | Meaning | Mutable? | Available for new planned execution? |
|---|---|---|---|
| `DRAFT` | The specification is under development and may be incomplete | Yes | No |
| `FROZEN` | The exact approved version is immutable | No | Only when `execution_eligibility` is `ELIGIBLE` |
| `RETIRED` | The immutable version is retained for history but unavailable for new planned execution | No | No |

Status records lifecycle and immutability. It does not establish scientific or execution eligibility by itself.

## 6. Execution eligibility

The `execution_eligibility` vocabulary is exactly:

| Value | Meaning |
|---|---|
| `ELIGIBLE` | The exact frozen test version has complete approved execution and assessment contracts and may be selected by an authorized manifest |
| `NOT_ELIGIBLE` | The version must not be selected for new planned execution |

`FROZEN` does not automatically mean `ELIGIBLE`; a test may be scientifically frozen yet non-executable. `DRAFT` and `RETIRED` specifications must be `NOT_ELIGIBLE`. Eligibility permits selection by a valid execution plan but does not itself create evidence eligibility, a finding, or a qualification decision.

## 7. Assessment requirements

Deterministic and human assessment requirements remain separate. A frozen eligible test may require:

- deterministic validation only;
- protocol-bound human assessment only; or
- both deterministic validation and protocol-bound human assessment.

Neither assessment type may be omitted from an eligible version when its acceptance criteria depend on that assessment. A specification requiring neither may exist only as a non-executable `DRAFT` with `execution_eligibility: NOT_ELIGIBLE`.

Deterministic requirements define mechanically assessable test-contract conditions. Human requirements identify the exact versioned assessment protocol required to evaluate human-judgment dimensions. Neither requirement may directly create final severity, qualification, or policy consequence.

## 8. Prohibited mechanisms and interpretations

A canonical `test_spec` must not define a canonical `hard_fail` or `hard_fail_type` mechanism, use `NO_DEPLOY` as an outcome, or automatically map test-level `PASS` or `FAIL` language to qualification. Test acceptance remains distinct from validator execution state, human findings, adjudicated severity, qualification outcome, and policy consequence.

The specification's `prohibited_interpretations` must prevent claims broader than the exact construct, applicability boundary, test version, and evidence generated under an authorized execution manifest.

## 9. Current v0.6.1 implementation status

The development-stage executable [`test_spec` schema](../schemas/v0.6.1/test_spec/test_spec.schema.json) and machine-readable structural vectors now exist. The vectors are not approved or canonical test-specification instances. Current Markdown test assets remain `DRAFT` and `NOT_ELIGIBLE` and have not been migrated into serialized canonical instances.

No approved canonical test-specification instance, runner, execution-manifest instance, model execution, evidence, validator execution, qualification, or gate execution exists.
