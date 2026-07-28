# CASEF v0.6.1 canonical execution-manifest contract

## 1. Purpose and authority

This document governs the documentation-level field and invariant contract for canonical `execution_manifest` records in CASEF v0.6.1.

`docs/canonical_evidence_contract.md` remains authoritative for record ownership and evidence-chain boundaries. Exact canonical `test_spec` contracts remain authoritative for test semantics. `docs/gates.md` remains the sole authority for evidence eligibility and qualification semantics. This contract is subordinate to all three sources within their respective authority.

This contract does not define JSON Schema, dispatch logic, retry implementation, storage, evidence results, or active gate rules.

## 2. Record ownership boundary

A canonical `execution_manifest` owns:

- planned execution identity and version;
- suite identity and suite version;
- exact selected test identities and versions;
- one planned target and interface;
- the planned execution protocol and conditions;
- repetitions and immutable planned execution slots;
- capture requirements;
- planned deterministic and human assessment requirements; and
- execution authorization state.

An `execution_manifest` must not own:

- test constructs, prompts, acceptance criteria, or other test semantics;
- actual model, product, provider, or interface observations;
- actual timestamps after an execution attempt begins;
- captured prompt or model-output content;
- validator execution results or deterministic findings;
- human findings;
- severity;
- qualification outcomes; or
- policy consequences.

Planned facts remain distinct from the observed facts later owned by `run_record`.

## 3. Field dictionary

| Field | Requirement | Meaning and constraints |
|---|---|---|
| `schema_version` | Required | Exact supported version of this documentation-level contract; distinct from manifest, suite, test, Context-of-Use, and downstream record versions |
| `manifest_id` | Required, non-null | Stable identity of one planned execution definition across its explicit versions |
| `manifest_version` | Required, non-null | Exact version of the planned execution definition; an authorized version is immutable |
| `suite_id` | Required | Stable identity of the selected test suite definition |
| `suite_version` | Required | Human-approved suite version owned by the manifest and bound to the exact `selected_test_references` |
| `execution_class` | Required | Exactly `QUALIFICATION_CANDIDATE` or `PLANNED_DIAGNOSTIC` |
| `context_of_use_reference` | Required for `QUALIFICATION_CANDIDATE` | Exact immutable Context-of-Use ID, version, reference, and hash; optional for `PLANNED_DIAGNOSTIC` only when no qualification claim is made |
| `selected_test_references` | Required, non-empty collection | Exact canonical test identity serialized as `record_id`, owner-specific `test_version`, specification reference, and specification hash for every selected test; `record_id` carries the canonical `test_id` |
| `planned_target` | Required | One requested target identity, preserving null where an identity element is not exposed rather than inferring it |
| `planned_interface` | Required | Exact planned interface or operating surface, distinct from later observed interface facts |
| `planned_execution_conditions` | Required | Controlled and declared conditions necessary to interpret the planned execution |
| `planned_generation_settings` | Required | Exact controlled generation settings, with explicit not-applicable or unknown handling where the interface does not expose control |
| `planned_tool_conditions` | Required | Planned tool availability and permissions relevant to the selected test contracts |
| `planned_session_conditions` | Required | Planned conversation, memory, and session-state conditions relevant to execution |
| `planned_run_slots` | Required, non-empty collection | Immutable planned repetitions, each with one unique `run_slot_id` and one exact selected test reference |
| `capture_requirements` | Required | Required source-artifact and provenance capture for each planned slot; does not contain captured evidence |
| `validation_requirements` | Required collection | Planned deterministic validation required by selected test specs; binds exact upstream test requirement IDs to slots without copying validator references or semantics |
| `rater_requirements` | Required collection | Planned human assessment required by selected test specs; binds exact upstream test requirement IDs to slots without copying rater-protocol references, rater counts, or semantics |
| `manifest_status` | Required | Exactly `DRAFT`, `AUTHORIZED`, `SUPERSEDED`, or `CANCELLED` |
| `prepared_by` | Required | Identity and role of the person or tooling that prepared the manifest; preparation is not execution or qualification authorization |
| `authorized_by` | Required for `AUTHORIZED`; conditional for `SUPERSEDED` or `CANCELLED` | Identity and role of the human authority approving the exact execution plan; absent for `DRAFT`; for a terminal lifecycle version, present together with `authorized_timestamp_utc` when the predecessor lineage was authorized and otherwise absent; null is prohibited |
| `prepared_timestamp_utc` | Required | Canonical UTC timestamp at which this manifest version was prepared |
| `authorized_timestamp_utc` | Required for `AUTHORIZED`; conditional for `SUPERSEDED` or `CANCELLED` | Canonical UTC timestamp of execution-plan authorization; absent for `DRAFT`; for a terminal lifecycle version, present together with `authorized_by` when the predecessor lineage was authorized and otherwise absent; null is prohibited |
| `supersedes_manifest_version` | Optional, and required for `SUPERSEDED` or `CANCELLED` | Earlier version of the same `manifest_id` replaced by this additive lifecycle version; absent when none exists; null is prohibited |
| `supersession_reason` | Conditionally required | Bounded reason for supersession; present if and only if `supersedes_manifest_version` is present; otherwise absent; null is prohibited |

Canonical manifest serialization uses field absence for inapplicable optional authorization and supersession states. Null is permitted only for the required planned-target identity elements where it has the explicit meaning defined below. String sentinels such as `"NONE"`, `"N/A"`, `"UNKNOWN"`, `"NULL"`, or `"NOT_PROVIDED"` must not substitute for null or field absence.

## 4. Executable nested structures

The development-stage executable schema freezes the following nested field structures. Every completed nested object is closed against undeclared fields.

### 4.1 References

`context_of_use_reference` composes the common versioned-contract reference base with:

- required `context_id`;
- required `context_version`;
- required `contract_reference`; and
- required `contract_hash`.

Context of Use is a referenced non-record contract input. It must not be typed as a canonical-record reference.

Each `selected_test_references` item composes the common record-reference base with:

- `record_type`, fixed to `test_spec`;
- required `record_id`, which carries the canonical `test_id`;
- required `test_version`;
- required `record_reference`; and
- required `record_hash`.

No duplicate `test_id` or `record_version` field is added. The collection is non-empty and set-like, keyed content-aware by `(record_id, test_version)`.

### 4.2 Planned target and interface

`planned_target` is a required object with all four fields:

- `provider_id`;
- `product_id`;
- `model_id`; and
- `model_alias`.

The first three fields are stable identifiers or null. `model_alias` is a non-blank string or null. At least one field must be non-null. Null is meaningful only when that identity element is not exposed or cannot be selected without inference.

`planned_interface` contains required stable identifiers `interface_id` and `interface_type_id`. Optional `interface_version` is a non-blank string and is absent when inapplicable. `interface_type_id` is owner-bound; this contract creates no universal platform taxonomy.

### 4.3 Planned conditions

`planned_execution_conditions` is a required set-like collection that may be empty. Each item contains required `condition_id` and `planned_value`.

`planned_generation_settings` contains:

- required `settings_state`, exactly `DECLARED`, `NOT_APPLICABLE`, or `NOT_EXPOSED`; and
- required set-like `settings`.

Each setting contains `setting_id` and `planned_value`. `DECLARED` requires at least one setting; the other states require an empty collection.

`planned_tool_conditions` contains:

- required `tool_mode`, exactly `NO_TOOLS` or `DECLARED_TOOLS`; and
- required set-like `tools`.

Each tool contains required `tool_id`, required `availability` of `ENABLED` or `DISABLED`, required set-like `permission_ids` that may be empty, and optional `tool_version`. `NO_TOOLS` requires an empty collection; `DECLARED_TOOLS` requires at least one tool.

`planned_session_conditions` contains:

- required `session_mode`, exactly `NEW_SESSION` or `CONTINUING_SESSION`;
- required `memory_mode`, exactly `DISABLED`, `ENABLED`, or `PLATFORM_MANAGED`;
- required `preexisting_context`, exactly `PROHIBITED`, `PERMITTED`, or `REQUIRED`; and
- required set-like `conditions`, which may be empty.

Every condition or setting `planned_value` is one non-null JSON string, number, or boolean. Semantic identity uniqueness is content-aware and uses `condition_id`, `setting_id`, or `tool_id` as applicable.

### 4.4 Planned slots

Each `planned_run_slots` item contains:

- required `run_slot_id`;
- required `test_record_id`;
- required `test_version`; and
- required positive-integer `repetition_index`.

The collection is non-empty and set-like, keyed content-aware by `run_slot_id`. The slot does not duplicate `manifest_id` or `manifest_version`; containment in the immutable manifest provides that binding.

### 4.5 Planned downstream requirements

`capture_requirements` is a required set-like collection. Each item contains:

- required `capture_requirement_id`;
- required non-empty set-like `run_slot_ids`;
- required non-empty set-like `artifact_roles`, using only `PROMPT_SOURCE`, `OUTPUT_SOURCE`, or `TRACE_SOURCE`; and
- required non-empty set-like `provenance_requirements`.

Each provenance requirement contains `requirement_id` and a bounded statement. These requirements do not list JSON field names or contain captured artifacts.

Each `validation_requirements` item contains only:

- required `requirement_id`;
- required `test_requirement_id`; and
- required non-empty set-like `run_slot_ids`.

Each `rater_requirements` item contains the same three fields. These structures bind upstream test requirement IDs to planned slots. They do not copy test identity, validator references or logic, rater-protocol references, assessment counts, criterion text, or expected results. The selected `test_spec` remains authoritative for validator and protocol references; the rater protocol remains authoritative for required-rater count.

### 4.6 Actors

`prepared_by` is a closed composition of the common actor-identity base and permits either `HUMAN` or `TOOL`. `authorized_by` is a closed composition of the common human-actor identity base and requires `actor_kind: HUMAN`. Neither structure creates a universal role enum or proves actual authority.

## 5. Selected-test binding

Every selection binds one exact canonical test version through `record_id` carrying the canonical `test_id`, owner-specific `test_version`, a content reference, and a content hash. A selected test must be `FROZEN` and `ELIGIBLE` under `spec/test_spec_contract.md` when the manifest is authorized.

The manifest does not copy or redefine the construct, prompt protocol, output contract, acceptance criteria, or assessment semantics. Fixed A/B, ordered multi-turn, and closed variant-set protocols remain one selected test version and one planned repetition; their internal steps do not become separate test identities.

`suite_version` and the exact selection set remain bound in the same manifest. A suite label or filename does not establish composition without those exact references.

## 6. Execution classes

The manifest `execution_class` vocabulary is exactly:

| Value | Meaning | Qualification use |
|---|---|---|
| `QUALIFICATION_CANDIDATE` | Planned execution that may later contribute evidence to one bounded qualification decision if every downstream eligibility requirement is satisfied | Potentially eligible; never qualified merely by manifest authorization |
| `PLANNED_DIAGNOSTIC` | Planned execution for debugging, research, or protocol development | Not canonical qualification evidence |

`UNPLANNED_DIAGNOSTIC` is an execution classification, not a third manifest class, because no canonical manifest owns an execution outside an authorized immutable manifest. Such an execution may be retained for diagnostics but cannot contribute canonical qualification evidence.

A `PLANNED_DIAGNOSTIC` execution cannot be retroactively promoted into qualification evidence by later assigning a different class, manifest, or Context of Use.

## 7. Manifest status and authorization

The `manifest_status` vocabulary is exactly:

| Value | Meaning | May start new planned execution? |
|---|---|---|
| `DRAFT` | Mutable execution plan not yet authorized | No |
| `AUTHORIZED` | Exact immutable execution-plan version approved for its declared execution class | Yes, subject to all declared preconditions |
| `SUPERSEDED` | Preserved version replaced through an explicit additive supersession relation | No |
| `CANCELLED` | Preserved plan withdrawn from new execution | No |

Only an exact immutable `AUTHORIZED` manifest version may support planned `QUALIFICATION_CANDIDATE` execution. Authorization freezes all owned planning facts, including target, interface, conditions, selections, requirements, and slots. A change to any of them requires an explicit new manifest version or manifest identity, as applicable. An `AUTHORIZED` version requires both authorization fields and at least one capture requirement.

Supersession or cancellation is represented by a new additive manifest version and must preserve the predecessor and any attempts already bound to it. `SUPERSEDED` and `CANCELLED` require `supersedes_manifest_version` and `supersession_reason`. Their authorization fields are either both present or both absent. When the predecessor lineage was authorized, its authorization provenance remains present and unchanged; when a never-authorized draft lineage is cancelled or superseded, those fields remain absent. Cross-record validation establishes the predecessor state, same-lineage relation, provenance preservation, and immutability of planning facts.

A never-authorized plan may receive a canonical `CANCELLED` lifecycle version. The additive lifecycle version does not authorize execution and does not rewrite an earlier immutable version.

Manifest authorization approves an execution plan only. It is not authorization of a finding, severity, qualification outcome, or policy consequence.

## 8. Planned execution slots

Every planned repetition has one immutable `run_slot_id` that is unique across canonical manifests. Each slot binds:

- the exact manifest identity and version;
- one exact selected `test_id` and `test_version`; and
- the planned repetition represented by that slot.

A future `run_record` references one exact `run_slot_id` together with its manifest binding. One slot cannot silently bind multiple execution attempts. If a new attempt is needed after execution begins, it requires a new run slot or a new manifest version according to the future executable retry policy.

If a precondition fails before an execution attempt begins, no `run_record` is created. The unfilled required slot remains visible as incomplete planned evidence downstream and must not be converted into adverse model behavior.

This contract does not define retry control flow, allocation storage, or runner behavior.

## 9. Context-of-Use binding

Every `QUALIFICATION_CANDIDATE` manifest requires one exact immutable `context_of_use_reference` governed by `spec/context_of_use.md`. The planned target, interface, conditions, and selected tests must be interpretable within that bounded Context of Use.

A `PLANNED_DIAGNOSTIC` manifest may omit the Context-of-Use reference only when no qualification claim is made. Assigning a Context of Use later does not retroactively make diagnostic execution canonical qualification evidence.

## 10. Planned requirements and downstream facts

`capture_requirements`, `validation_requirements`, and `rater_requirements` state what must later be produced or performed. They reference the exact selected test contracts and applicable protocols without copying their semantics.

An absent required run, capture, validation, or rating remains an unresolved downstream evidence requirement. It does not become a model finding, test-constraint failure, or qualification outcome inside the manifest.

The manifest must never contain observed execution timestamps, captured artifact content, conformance results, deterministic or human findings, severity, qualification outcome, or policy consequence.

## 11. Structural and content-aware validation boundary

The executable schema enforces object shape and closure, enums, lexical references and hashes, requiredness, null-versus-absence rules, lifecycle and execution-class conditionals, basic collection cardinality, and actor kind.

Content-aware validation remains responsible for referent existence, content-hash agreement, selected-test `FROZEN` and `ELIGIBLE` state, suite composition, slot-to-test agreement, semantic identity uniqueness, full capture and assessment coverage, Context-of-Use compatibility, actual authorization authority, timestamp ordering, predecessor lineage, immutable-plan preservation, diagnostic non-promotion, and prevention of slot reuse across attempts.

Structural schema success does not establish any content-aware fact, execution success, evidence eligibility, qualification, or use permission.

## 12. Current v0.6.1 implementation status

The development-stage executable [`execution_manifest` schema](../schemas/v0.6.1/execution_manifest/execution_manifest.schema.json) and machine-readable structural vectors now exist. The vectors are not canonical manifest instances or execution authorization.

No canonical manifest instance, runner, retry policy, cross-record validator, rater protocol execution, model or API execution, captured artifact, evidence, gate execution, or qualification capability is created.
