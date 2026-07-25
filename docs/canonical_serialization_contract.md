# CASEF v0.6.1 canonical serialization and version-namespace contract

## 1. Purpose and authority

This document is the sole CASEF v0.6.1 authority for canonical serialized wire format, text encoding, future JSON Schema dialect and identity, lexical version rules, the identifier lexical envelope, missing-value representation, timestamp normalization, collection-ordering categories, reference serialization boundaries, content hashes, JSON canonicalization, schema compatibility and supersession, and the structural validation-error format.

It is subordinate to canonical evidence ownership and qualification and gate semantics. It does not change the six-record architecture, create a seventh canonical record, or define scientific validity, evidence eligibility, gate policy, final severity, qualification, or policy consequence.

Authority is ordered as follows:

1. [`docs/canonical_evidence_contract.md`](canonical_evidence_contract.md) governs record ownership and evidence-chain boundaries.
2. [`docs/gates.md`](gates.md) governs qualification and gate semantics.
3. This document governs serialization within its bounded authority.
4. The exact record or referenced-input contract governs object-owned fields and semantics.
5. Future executable schemas and implementations remain subordinate implementations.

When serialization and record semantics interact, record ownership remains with the record-specific contract. This document controls only the machine representation of that meaning.

This document remains a documentation-level authority. Development-stage executable JSON Schemas now exist as subordinate implementations; their structural success does not expand this contract's authority.

## 2. Canonical data format and encoding

The canonical serialized format is JSON encoded as UTF-8 without a byte-order mark. A byte-order mark is prohibited.

YAML, TOML, CSV, Markdown, and database rows are not canonical record encodings. They may later serve as authoring or viewing formats only when converted into canonical JSON through an explicitly versioned process. A textual representation is not canonical merely because it contains equivalent information.

Canonical evidence references bind the resulting canonical JSON or exact source-artifact bytes, not an untracked equivalent representation.

## 3. JSON Schema dialect and identity

CASEF executable schemas use JSON Schema Draft 2020-12. Every root schema must contain `$schema`, `$id`, `title`, and `type`. The `$schema` value is `https://json-schema.org/draft/2020-12/schema`.

The versioned schema-directory convention is:

- `schemas/v0.6.1/common/`
- `schemas/v0.6.1/test_spec/`
- `schemas/v0.6.1/execution_manifest/`
- `schemas/v0.6.1/run_record/`
- `schemas/v0.6.1/validation_record/`
- `schemas/v0.6.1/rater_protocol/`
- `schemas/v0.6.1/rater_record/`
- `schemas/v0.6.1/context_of_use/`
- `schemas/v0.6.1/qualification_record/`

The `schemas/v0.6.1/common/` directory contains development-stage executable scalar, hash, reference-base, repository-provenance, and actor-identity schemas. The `schemas/v0.6.1/test_spec/` directory contains the first complete canonical-record schema. The remaining record-specific schema directories remain unimplemented. These schemas use their future immutable release-tag `$id` values but are not represented as released until the immutable `v0.6.1` Git tag exists.

Future released `$id` values use immutable release-tag paths in this form:

`https://raw.githubusercontent.com/sergey-morev/CASEF-Clinical-AI-Safety-Evaluation-Framework/v0.6.1/schemas/v0.6.1/<path>.schema.json`

Released `$id` values are immutable. A released schema must not use `main` in its `$id`. During development, a local schema catalog may map the final immutable `$id` to working-tree files. The immutable release tag must exist before a schema is represented as released. Relative `$ref` resolution must remain within the versioned schema tree unless an exact external immutable schema is intentionally referenced.

Future composed full-object schemas close their completed object boundary with `unevaluatedProperties: false`. `additionalProperties: false` is used only where it is composition-safe for the exact local object.

No generic extension container is authorized in v0.6.1. New fields require a schema revision.

## 4. Object-key and string rules

Canonical JSON object keys use lowercase `snake_case`.

Required identifier, reference, and bounded-rationale strings must:

- be strings;
- be non-empty;
- contain at least one non-whitespace character; and
- contain no leading or trailing whitespace.

This contract does not impose one universal maximum length on every semantic text field. Exact schemas define bounded lengths appropriate to the field owner.

Empty strings must not substitute for missing values. Sentinel strings such as `NONE`, `N/A`, `UNKNOWN`, `NULL`, and `NOT_PROVIDED` must not substitute for null or field absence unless an exact owner defines the value as controlled vocabulary.

## 5. Missing values, null, and field absence

Canonical emission follows these rules:

1. An optional value that is not present is omitted.
2. `null` is used only when the field is required to remain present and the exact contract explicitly permits `null` as a meaningful state.
3. A schema must not generically permit both `null` and absence for every optional field.
4. Empty strings, empty objects, and sentinel strings are not missing-value substitutes.
5. Empty collections are valid only where the owning contract expressly permits them.
6. A required non-empty collection uses `minItems: 1`.
7. A required collection that may be empty remains present as `[]`.

These rules narrow canonical output without altering record-specific ownership or controlled vocabularies.

## 6. Identifier rules

The shared lexical envelope for stable public identifiers is:

`^[A-Za-z][A-Za-z0-9._:-]{0,127}$`

Identifiers are case-sensitive, and whitespace is prohibited. Filenames, headings, and display labels are not authoritative identity. Each object-specific schema may narrow the pattern.

This contract does not require UUIDv7, UUIDv4, ULID, or another single generation algorithm. An implementation generating record IDs must provide collision-resistant stable identities. Generated-ID strategy remains an implementation decision until a later contract explicitly narrows it.

Existing stable role IDs and test-style IDs remain compatible when they satisfy this envelope.

## 7. Version namespaces

The following namespaces are semantically distinct:

- `schema_version`
- `test_version`
- `construct_version`
- `manifest_version`
- `suite_version`
- `record_version`
- `validator_version`
- `rater_protocol_version`
- `context_version`
- `gate_policy_version`
- `finding_or_construct_version`
- `transformation_policy_version`
- `vocabulary_version`
- `rubric_version`
- `tool_or_process_version`

Lexical equality does not transfer ownership or merge namespaces. A version string for one concept must not be reused as proof of another concept's version.

### Authored version grammar

Authored schemas, contracts, protocols, policies, constructs, vocabularies, tools, and suites use this SemVer-like grammar:

`^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$`

Conforming examples include `v0.6.1`, `v0.3.0-draft`, and `v1.2.0-rc.1`. Build metadata using `+` is not part of the v0.6.1 canonical grammar.

Current documentation assets do not become conforming serialized instances merely because they contain version-like text. Any future migration must emit values conforming to the applicable canonical namespace.

### Record lineage version

`record_version` is a positive integer starting at `1`.

A metadata correction increments the lineage according to the owning record contract. A new execution, reassessment, revalidation, or decision may require a new record identity rather than merely incrementing the prior record version.

### Compatibility meaning

For `schema_version`:

- a major change is a backward-incompatible serialized-contract change;
- a minor change is a backward-compatible additive optional capability; and
- a patch change is a clarification or correction that does not alter valid serialized meaning.

Other version namespaces remain governed by their owning contracts. Shared lexical syntax does not impose identical lifecycle or compatibility semantics. Project release version and `schema_version` may have the same lexical value but remain distinct concepts.

## 8. Timestamp representation

Canonical timestamps use RFC 3339 UTC with uppercase `Z`. Non-zero UTC offsets are not canonical output, and the date and time separator is uppercase `T`.

Whole seconds use `YYYY-MM-DDTHH:MM:SSZ`. Fractional seconds are omitted when zero. When non-zero, one through nine fractional digits may be emitted, and trailing fractional zeroes are removed.

Canonical examples are:

- `2026-07-21T11:32:39Z`
- `2026-07-21T11:32:39.125Z`
- `2026-07-21T11:32:39.000004Z`

Leap-second handling is deferred to the future implementation and must not be silently normalized. Timestamps preserve observed or authored precision and must not fabricate greater clock accuracy.

## 9. Numeric representation

Canonical JSON permits only finite JSON numbers. Integral quantities use JSON integers. `NaN`, positive infinity, and negative infinity are prohibited.

Precision-sensitive decimal quantities use owner-defined decimal strings when binary floating-point would alter intended meaning. Numeric range, unit, and precision remain owned by the exact field contract. Implementations must not silently coerce numeric strings into numbers or numbers into strings.

## 10. Collection ordering and duplicates

Every future array field is classified by its owning schema as either `ORDERED_SEQUENCE` or `SET_LIKE_COLLECTION`.

Ordered sequences preserve exact observed, planned, or presented order. Reordering an ordered sequence changes canonical content and its hash.

Set-like collections have no semantic order. A future canonical emitter must sort each set-like collection using an exact owner-defined stable key before hashing. No global sorting key is inferred.

Duplicate semantic identities are prohibited unless an exact contract explicitly permits repetition. JSON Schema `uniqueItems` may supplement structural validation but does not replace semantic-identity duplicate checking.

This classification does not modify current Markdown contracts.

## 11. Enum ownership

Common schemas may inline only vocabularies already owned globally by current canon. Protocol-, validator-, test-, or gate-policy-owned vocabularies must be resolved through exact versioned references.

A downstream record schema must not copy an external owner's evolving vocabulary and thereby become a competing authority. Structural schemas may validate the shape of an externally owned response while cross-record validation confirms that the value is admitted by the exact referenced owner.

## 12. Reference serialization boundary

Future executable references use composition, not one universal reference object.

### Record-reference base

A canonical-record reference binds:

- `record_type`;
- `record_id`;
- `record_version`, where defined by the referenced record contract;
- `record_reference`; and
- `record_hash`.

### Artifact-reference base

An artifact reference binds:

- `artifact_reference`; and
- `artifact_hash`.

Future schemas may additionally require `media_type`, `byte_length`, and `artifact_role` only where the owner requires them.

### Versioned-contract-reference base

A versioned referenced input binds:

- the stable owner-specific ID;
- the exact owner-specific version;
- `contract_reference`; and
- `contract_hash`.

Specialized references may add `repository_commit`, `implementation_reference`, `implementation_hash`, `protocol_commit`, or `gate_policy_commit` when required by the exact owner.

Test, manifest, validator, rater-protocol, Context-of-Use, and gate-policy references remain specialized compositions. A protocol or Context-of-Use reference must not be typed as a canonical-record reference. Reference presence does not transfer ownership, and references must bind exact immutable content.

The development-stage [`schemas/v0.6.1/common/references.schema.json`](../schemas/v0.6.1/common/references.schema.json) now defines the common base key sets for the three distinct reference families. These bases are composition components, not universal complete reference objects. Owner-specific stable IDs, exact versions, and authorized supplemental fields remain specialized. Final completed owner-specific objects close their boundary with `unevaluatedProperties: false`; direct validation against a base establishes only the common base obligations and is not complete-reference validation.

## 13. Reference locators

A canonical content locator is an absolute URI. For repository-owned content, exact provenance additionally binds `repository_commit` and `repository_path`.

For CASEF v0.6.1 executable repository provenance:

- `repository_commit` is a full 40-character lowercase hexadecimal Git commit object ID; branch names and abbreviated SHAs are insufficient; and
- `repository_path` is a non-empty repository-root-relative forward-slash path with no leading slash, backslash, whitespace, empty segment, `.` or `..` segment, or trailing slash.

A commit change or Git object-format migration requires a reviewed schema revision. Repository provenance does not replace the applicable absolute URI or content hash. The URI, commit, and path must resolve to the same intended content. Lexical path validity does not prove existence, content correctness, or authority.

### Actor representation

The shared actor-base keys are:

- `actor_id`;
- `actor_kind`; and
- `role_id`.

`actor_kind` is exactly `HUMAN` or `TOOL`. CASEF v0.6.1 creates no universal global `role_id` enum; exact record and protocol owners narrow or const-bind roles. Role-bound actor bases remain compositional, and final owner-specific objects close their completed boundary.

Personal names and direct contact fields are not part of public operational actor identity. Actor identity alone does not establish authority, eligibility, expertise, independence, approval, or successful execution.

## 14. Hash representation and algorithm

CASEF v0.6.1 canonical content hashes use SHA-256 and serialize as `sha256:<64 lowercase hexadecimal characters>`.

For example:

`sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef`

The algorithm prefix is mandatory. Uppercase hexadecimal and a bare digest are non-canonical. A hash-algorithm change requires a later serialization-contract revision.

A hash establishes content integrity only. It does not prove authenticity, provider identity, scientific validity, expertise, eligibility, or decision authority.

## 15. JSON canonicalization and record hashing

Canonical JSON objects are canonicalized using RFC 8785 JSON Canonicalization Scheme before record or derived-input hashing.

Canonicalization does not alter semantic fields. String Unicode content and object-member ordering follow RFC 8785. Array order is preserved after owner-required set-like normalization.

Self-referential hash fields are prohibited in canonical v0.6.1 record payloads. `record_hash` is stored by the referencing object or evidence envelope, not inside the record payload being hashed.

The record hash is SHA-256 over the RFC 8785 canonical bytes of the exact immutable record object. Transport metadata outside the canonical record object is excluded.

This contract does not implement RFC 8785.

## 16. Source-artifact hashing

Source artifacts are hashed over exact stored bytes. Source-artifact hashing does not perform Unicode normalization, newline normalization, whitespace trimming, decoding and re-encoding, rendering cleanup, metadata injection, redaction, or compression transformation before hashing the canonical source artifact.

A transformed, normalized, redacted, or rendered derivative is a separate artifact with its own identity, its own hash, an exact canonical source reference, an exact transformation-policy reference, and transformation provenance.

## 17. Derived input-set hashes

Derived input-set hashes use RFC 8785 canonical JSON objects with explicit domain separation.

The v0.6.1 domain tags are:

- `CASEF-VALIDATION-INPUT-v1`
- `CASEF-ASSESSMENT-INPUT-v1`
- `CASEF-DECISION-INPUT-v1`

The canonical domain object contains `hash_domain`, `ordered_input_references`, and owner-required protocol, presentation, or policy bindings.

The validation input hash binds exact validation inputs and validator binding. The assessment input hash binds exact ordered assessment inputs, rater protocol, and evidence presentation. The decision input hash binds exact included and excluded inputs, Context of Use, and gate-policy binding.

Concatenating raw hashes without a structured domain object is prohibited. Exact object schemas are deferred to later executable-schema tasks.

## 18. Schema compatibility and supersession

Released schema `$id` values are immutable. Content must not be replaced under an existing released `$id`; a released `$id` must not point at `main`; and an older schema version must not be silently reinterpreted.

A future schema catalog records:

- `schema_id`;
- `schema_version`;
- `schema_reference`;
- `schema_hash`;
- `supersedes_schema_id`, where applicable; and
- `supersession_reason`, where applicable.

A superseded schema remains resolvable for historical evidence. Schema supersession does not supersede records validated under the earlier schema.

No schema catalog is created by this contract.

## 19. Structural validation errors

Future schema validation emits a machine-readable result containing:

- `validator_id`;
- `validator_version`;
- `schema_id`;
- `validation_status`; and
- `errors`.

Each structural error contains:

- `error_code`;
- `instance_path`;
- `schema_path`; and
- `bounded_message`.

Paths use JSON Pointer. `error_code` is stable and machine-readable, and messages are bounded explanatory text. Library-native exception text alone is not a canonical validation result.

Structural validation errors do not automatically become adverse model findings. Validation success does not establish scientific validity, evidence eligibility, or qualification. Exact executable schemas and an error-result JSON Schema are deferred.

## 20. Historical and candidate material

The following sources must not silently dictate canonical serialization:

- `measurement/log_schema.md`
- `measurement/conversation_audit_schema.md`
- `measurement/rater_labels.md`
- `measurement/risk_map.md`
- `measurement/artifact_taxonomy.md`
- `spec/model_registry.md`
- `spec/prompt_registry.md`
- current `DRAFT` test assets

They may serve only according to their current canonical status as historical material, a candidate payload, a subordinate vocabulary, or future migration input. Field names or enums from these files become canonical serialization only through an explicit authoritative contract or later reviewed schema.

## 21. Current implementation boundary

All six canonical record contracts and the canonical serialization decisions are documented. Development-stage common scalar, hash, reference-base, repository-provenance, and actor-identity JSON Schemas and their machine-readable valid and invalid test vectors exist. The first complete canonical-record schema, `test_spec`, and its structural vectors also exist.

A committed local development harness dynamically validates the versioned schema tree and vectors through an explicit no-network registry. A minimal GitHub Actions workflow runs that harness and its unit tests.

No schema catalog, canonical serializer, RFC 8785 implementation, SHA-256 computation or verification implementation, executable cross-record validator, serialized canonical record instance, or canonical evidence-generation workflow exists. The other five canonical record schemas remain unimplemented.

No approved rater-protocol or gate-policy instance exists, and no canonical qualification pipeline is executable.
