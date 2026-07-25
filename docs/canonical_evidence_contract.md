# CASEF v0.6.1 canonical evidence contract

## 1. Purpose and authority

This document is the authoritative source for canonical record ownership and evidence-chain boundaries in CASEF v0.6.1.

`docs/gates.md` remains the sole authority for qualification and gate semantics. This document does not redefine qualification outcomes, policy consequences, severity rules, or gate precedence. Neither document replaces the other within the other's authority.

[`docs/canonical_serialization_contract.md`](canonical_serialization_contract.md) is the sole authority for canonical wire format, lexical version rules, reference serialization, timestamp normalization, content hashes, and canonicalization. It is subordinate to this document's record-ownership authority and to the qualification authority of `docs/gates.md`; it does not alter record ownership or gate semantics.

The contract defines architecture only. It does not make the CASEF pipeline executable.

## 2. Six-record evidence chain

The canonical evidence chain contains exactly six record types:

1. `test_spec`
2. `execution_manifest`
3. `run_record`
4. `validation_record`
5. `rater_record`
6. `qualification_record`

Their relationship is:

**test contract → planned execution → observed execution → deterministic and protocol-bound human assessment → authorized qualification decision**

Conversation audit is a protocol-defined subtype or payload of `rater_record`, not a seventh canonical record. Raw prompt and output artifacts, Context-of-Use specifications, gate policies, validator definitions, and rater protocols are referenced inputs; they are not additional evidence-record types.

## 3. Record ownership

| Canonical record | Owns | Must not own |
|---|---|---|
| [`test_spec`](../spec/test_spec_contract.md) | Stable test identity and version; construct; exact versioned prompt protocol; acceptance criteria; assessment mode; execution eligibility | Suite membership, planned target, execution observations, findings, severity, or qualification |
| [`execution_manifest`](../spec/execution_manifest_contract.md) | Planned target and execution protocol; planned execution context; selected exact test versions; planned repetitions; controlled execution conditions; execution authorization state | Test semantics, actual observations, captured outputs, validation results, human findings, or qualification |
| [`run_record`](../measurement/run_record_schema.md) | One execution attempt; actual timestamps and execution outcome; observed target and context; captured source-artifact references and hashes | Manifest-conformance verdicts, deterministic or human findings, severity, or qualification |
| [`validation_record`](../measurement/validation_record_schema.md) | One deterministic validation execution; exact immutable input binding; validator identity; mechanically established checks and findings | Human judgment, individual or final severity, policy consequence, or qualification |
| [`rater_record`](../measurement/rater_record_schema.md) | One human-assessment execution; exact protocol identity; exact evidence presentation; rater identity; protocol-bound human findings; optional protocol-bound individual severity | Deterministic findings rewritten as human findings, multi-rater adjudication, final severity, policy consequence, or qualification |
| `qualification_record` | Evidence inclusion and exclusion; adjudicated findings; final severity where applicable; qualification outcome; Context-of-Use policy consequence; decision authority and provenance | Raw evidence content, rewritten upstream records, hidden model identity, or claims broader than the exact decision context |

No record may silently absorb the responsibilities of another. Referencing an owned fact does not transfer ownership.

`spec/test_spec_contract.md`, `spec/execution_manifest_contract.md`, `measurement/run_record_schema.md`, `measurement/validation_record_schema.md`, and `measurement/rater_record_schema.md` define the documentation-level field and invariant contracts for their respective canonical record types. `spec/rater_protocol_contract.md` defines the separate versioned protocol boundary for human assessment. They do not alter the ownership boundaries in this table.

## 4. Immutable evidence and derived judgment

Captured source artifacts record the exact prompt messages sent and model outputs observed. They are immutable after capture and are referenced by artifact identity, reference, and hash. An authored prompt contract in `test_spec` and the exact sent-prompt artifact in `run_record` are distinct facts.

Canonical terminal records are immutable. Deterministic validation, human assessment, adjudication, and qualification are derived from immutable inputs, but their resulting records are themselves permanent attributed records. Re-running or reinterpreting an input creates a new downstream record; it does not overwrite prior history.

Deterministic findings and human findings remain source-distinct. A validation result cannot be relabeled as human judgment, and a rater observation cannot be stored as a deterministic validator fact.

## 5. Allowed cross-record references

A cross-record reference must bind the exact immutable input with:

- `record_type`;
- `record_id`;
- `record_version`, where the referenced contract defines one; and
- `record_hash`.

An artifact binding must include:

- `artifact_reference`; and
- `artifact_hash`.

Record-specific contracts may require additional identity fields, such as exact test, manifest, protocol, validator, Context-of-Use, or gate-policy versions. These additions strengthen the binding; they do not create a competing owner for the referenced fact.

Mechanically copied identifiers are permitted only as checkable reference data. The referenced owner remains authoritative.

The executable representation of these references is governed by [`docs/canonical_serialization_contract.md`](canonical_serialization_contract.md). Record-specific meaning and requirement levels remain governed by the owning record contract.

## 6. Prohibited duplication and ownership conflicts

Canonical records must not:

- embed raw prompt or output content in multiple records;
- copy complete upstream records instead of referencing them;
- overwrite planned target identity with observed identity, or observed identity with planned identity;
- store manifest conformance in `run_record`;
- store human judgment in `validation_record`;
- store final severity or qualification outside `qualification_record`;
- turn a stimulus annotation into an adverse model finding;
- treat filenames as authoritative record, test, model, or artifact identity;
- create provider-wide, company-wide, product-wide, permanent-model, or general-safety conclusions from bounded evidence; or
- use one mixed record as a substitute for the six-record evidence chain.

Optional missing values use actual null or field absence only where the record-specific contract permits it. Empty strings and sentinel strings such as `"NONE"`, `"N/A"`, or `"UNKNOWN"` must not substitute for missing-data semantics unless a field explicitly defines that value as controlled vocabulary.

## 7. Record identity and versioning

Each canonical record instance has a stable record identity and binds the exact schema or contract version used to produce it. A version identifier for one concept must not be reused for another: schema version, test version, manifest version, record version, Context-of-Use version, validator version, rater-protocol version, and gate-policy version remain distinct.

Lexical version rules and the machine representation of record identity are governed by [`docs/canonical_serialization_contract.md`](canonical_serialization_contract.md). This document continues to govern identity ownership and immutability.

Once terminal, a record is immutable. A correction, invalidation, revalidation, reassessment, or reevaluation creates a new immutable record identity and an explicit supersession or replacement relation. Previous records remain discoverable.

A materially changed test contract, Context of Use, planned target, or execution protocol cannot be retroactively applied to evidence captured under an earlier version.

## 8. Artifact and hash provenance

Artifact and record hashes bind exact immutable content. The canonical hash algorithm, hash representation, JSON canonicalization rule, and exact-byte source-artifact hashing rule are governed by [`docs/canonical_serialization_contract.md`](canonical_serialization_contract.md).

Record-specific contracts define which owned content and hash-bearing fields their objects require; they do not independently select competing hash algorithms or canonicalization rules. Integrity processing must not modify the captured source artifact.

A hash establishes integrity of referenced bytes; it does not prove provider identity, model authenticity, or correctness of the content.

If a redacted or transformed derivative is presented, it requires its own artifact identity and hash plus an explicit reference to the canonical source artifact and transformation policy. A derivative never silently replaces canonical source evidence.

## 9. Supersession and reevaluation

Supersession is additive. A superseding record identifies the prior record, the reason for supersession, the authority or producer responsible, and the time of the new action. The prior record is never deleted or silently amended.

A changed upstream input requires a new downstream record. In particular:

- a new run-record version or corrected artifact binding requires new validation and any required new human assessment;
- changed validator code produces a new `validation_record`;
- changed evidence presentation or rater protocol produces a new `rater_record`; and
- changed evidence inputs, Context of Use, gate policy, or decision execution produces a new `qualification_record`.

Reevaluation does not imply that a new model execution is always required. Whether new execution evidence is required depends on which immutable input changed and on the applicable test and gate policy.

## 10. Relationship to gate semantics

This document governs what records exist, which facts each record owns, and how exact inputs are referenced.

`docs/gates.md` governs evidence eligibility, finding admission, adjudicated severity, qualification outcomes, and Context-of-Use policy consequences. A `qualification_record` must bind the exact gate-policy identity, version, and repository commit that authorized its decision.

`spec/test_spec_contract.md`, `spec/execution_manifest_contract.md`, `measurement/run_record_schema.md`, `measurement/validation_record_schema.md`, `measurement/rater_record_schema.md`, and `measurement/qualification_record_schema.md` define the documentation-level field and invariant contracts for all six canonical record types. `spec/context_of_use.md` defines the minimum Context-of-Use specification, and `spec/rater_protocol_contract.md` defines the versioned protocol boundary for human assessment. All remain subordinate to the ownership and gate-authority boundaries above.

When these records are consumed for a decision, the authoritative path remains exactly:

**eligible evidence → deterministic and human findings → adjudicated severity where applicable → qualification outcome → Context-of-Use policy consequence**

This document creates no active blocking rule.

## 11. Current v0.6.1 implementation status

CASEF v0.6.1 retains documentation-level six-record ownership and gate boundaries. All six canonical record contracts and the canonical serialization contract are documented; Context of Use and the rater-protocol contract are documented separately. Development-stage common schemas now exist, and one of the six canonical record schemas is implemented: `test_spec`. The other five canonical record schemas remain unimplemented.

No canonical test-specification instance or evidence chain exists. No executable owner-specific validator or rater protocol, serializer, hash implementation, storage, dispatch, runner, evidence generation, automated qualification, or canonical qualification pipeline exists.

No canonical qualification pipeline is executable until required protocol instances, tooling, validation, and PI-approved gate rules are implemented and reviewed.
