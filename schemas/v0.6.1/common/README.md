# CASEF v0.6.1 common executable schema definitions

## Scope

This directory contains the first executable CASEF schema artifacts: reusable common scalar, hash, reference-base, repository-provenance, and role-bound actor-identity definition libraries using JSON Schema Draft 2020-12.

The definitions are subordinate to [`docs/canonical_serialization_contract.md`](../../../docs/canonical_serialization_contract.md). They implement lexical and structural rules only and own no canonical record content, evidence eligibility, gate semantics, or qualification authority.

## Files

- `scalars.schema.json` defines the shared identifier, authored-version, record-lineage version, canonical UTC timestamp, absolute-URI, and JSON-Pointer lexical forms.
- `hashes.schema.json` defines the SHA-256 digest component, canonical CASEF content-hash representation, and input-hash domain vocabulary.
- `references.schema.json` defines common record-, artifact-, and versioned-contract-reference composition bases plus repository-provenance primitives.
- `actors.schema.json` defines role-bound human and tool actor-identity composition bases.
- `tests/scalars_cases.json` contains machine-readable valid and invalid values for each scalar definition.
- `tests/hashes_cases.json` contains machine-readable valid and invalid values for each hash definition.
- `tests/references_cases.json` contains machine-readable valid and invalid values for each common reference and repository-provenance definition.
- `tests/actors_cases.json` contains machine-readable valid and invalid values for each common actor definition.

## Definition and composition behavior

Each schema root is a closed empty object used as a definition container. Consumers reference exact `$defs` fragments. Validating `{}` against a root has no record-level meaning, and these files are not canonical record schemas.

Scalar and hash fragments are complete scalar definitions. `record_reference_base`, `artifact_reference_base`, `versioned_contract_reference_base`, and the actor identity bases are open composition components. Direct validation against a base checks only its shared obligations. Owner-specific schemas explicitly declare authorized additions and close the completed object with `unevaluatedProperties: false`.

Composition-base openness is not a generic extension mechanism and does not authorize arbitrary canonical fields.

## Reference boundary

The common schema keeps exactly three reference families: canonical-record references, artifact references, and versioned-contract references. Record and artifact references remain distinct from versioned contracts. Protocol and Context-of-Use references are not canonical-record references, and reference presence does not transfer ownership.

Repository provenance supplements, but does not replace, the applicable absolute locator and content hash.

## Actor boundary

Public operational actor identities use stable actor IDs and role IDs. No personal-name field exists in the common actor base; any private controlled identity mapping remains outside the public repository.

Exact owner-specific schemas define qualifications, approval basis, eligibility, conflicts, independence, and authority. A tool identity cannot authorize qualification.

## Development and release state

The schemas use their future immutable release-tag `$id` values. They remain development artifacts until the immutable `v0.6.1` Git tag exists. No released-schema claim is made, and no schema catalog exists.

## Validation boundary

Lexical schema success does not prove semantic correctness. In particular:

- the timestamp regular expression does not establish full calendar validity or settle leap-second semantics;
- URI validity does not prove locator correctness, content integrity, or authority;
- hash-pattern validity does not compute or verify a digest;
- cross-file reference resolution does not prove owner-specific reference completeness, referent existence, authenticity, evidence eligibility, or authority; and
- no RFC 8785 canonicalization or SHA-256 computation implementation is included.

Local development validation requires an explicit registry that maps each immutable future `$id` to its working-tree schema. It must not depend on network retrieval.

## Test vectors

Each test-vector file names the exact schema `$id` and provides one case group per referenced `$defs` fragment. Every value in `valid` must validate against that fragment. Every value in `invalid` must produce at least one validation error. URI vectors must be checked with Draft 2020-12 URI format validation enabled.

The vectors are lexical and structural test data, not canonical records or evidence.

## Next dependency layer

The first complete canonical-record schema, `test_spec`, now exists and composes these common definitions. Specialized owner-specific schemas and the remaining five canonical record schemas remain deferred. The common definitions remain subordinate reusable components and do not acquire record ownership.
