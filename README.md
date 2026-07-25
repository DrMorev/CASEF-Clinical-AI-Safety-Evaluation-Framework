# CASEF — Clinical AI Safety Evaluation Framework

Physician-led qualification framework for LLM behavior in clinical-like and other high-stakes settings.

**Core idea:**  
CASEF treats LLM safety as a **qualification problem**, not a vibe, benchmark score, or alignment claim.

It provides a reproducible structure for evaluating model behavior under explicit constraints using:

**spec → measurement → gates → evidence**

CASEF is **model-agnostic** and **platform-portable** across apps, web UIs, and APIs.  
It focuses on **reproducible external evaluation artifacts**, not internal telemetry.

---

## Why CASEF exists

Most LLM evaluation still overweights answer quality and underweights **deployment-relevant failure**.

In real use, especially in clinical and other high-stakes environments, the question is not only:

- *Can the model produce a plausible answer?*

but:

- *Does it stay within role and constraints?*
- *Does it fabricate actions or certainty?*
- *Does it fail safely when information is missing?*
- *Can its behavior be logged, reviewed, and defended?*

CASEF is designed for this layer.

It is not a benchmark leaderboard.  
It is a framework for structuring evidence for bounded qualification decisions.

---

## What CASEF evaluates

CASEF is intended for failures that matter in deployment, not just benchmark performance.

Examples include:

- format violations under explicit constraints
- hallucinated actions or unsupported claims
- unsafe reassurance
- abstain / escalate failures
- role drift under pressure
- inconsistency between stated policy and observed behavior
- artifact-level failures that break reproducibility or reviewability

---

## What makes CASEF different

Unlike benchmark-style evaluation, CASEF focuses on **portable, inspectable qualification artifacts**:

- explicit test specs
- structured logging
- artifact taxonomy
- redaction rules
- model/platform registry
- requirements for reproducible evidence packs
- bounded qualification-decision review surfaces

The goal is not to ask whether a model is “good.”  
The goal is to ask whether a behavior is **acceptable for a defined context of use**.

---

## Scope

CASEF is currently designed as a framework for:

- clinical AI reliability evaluation
- high-stakes conversational system qualification
- platform-agnostic behavioral testing
- evidence-oriented safety review
- pre-deployment or controlled evaluation workflows

---

## Non-goals

- No jailbreak content
- No claims about internal model telemetry
- No claims of clinical deployment readiness by default
- Not medical advice
- Not an AI doctor
- Not a productized monitoring platform
- Not a replacement for domain governance, QA, or regulatory review

---

## Current design principles

- **Observed > claimed**
- **External behavior over internal speculation**
- **Reproducibility over intuition**
- **Failure visibility over vague optimism**
- **Qualification over hype**
- **Model-agnostic evaluation over vendor lock-in**

---

## Repository contents (v0.6.1 contract foundation)

### Canonical authority and contracts
- [`docs/canonical_evidence_contract.md`](docs/canonical_evidence_contract.md) — six-record ownership and evidence-chain authority
- [`docs/canonical_serialization_contract.md`](docs/canonical_serialization_contract.md) — documentation-level canonical wire-format, version-namespace, reference, timestamp, canonicalization, and hashing authority
- [`docs/gates.md`](docs/gates.md) — sole qualification and gate-semantics authority
- [`spec/test_spec_contract.md`](spec/test_spec_contract.md) — documentation-level canonical test-specification contract
- [`spec/execution_manifest_contract.md`](spec/execution_manifest_contract.md) — documentation-level canonical planned-execution contract
- [`measurement/run_record_schema.md`](measurement/run_record_schema.md) — documentation-level canonical observed-execution contract
- [`measurement/validation_record_schema.md`](measurement/validation_record_schema.md) — documentation-level canonical deterministic-validation contract
- [`spec/rater_protocol_contract.md`](spec/rater_protocol_contract.md) — documentation-level versioned human-assessment protocol boundary
- [`measurement/rater_record_schema.md`](measurement/rater_record_schema.md) — documentation-level canonical individual human-assessment execution contract
- [`spec/context_of_use.md`](spec/context_of_use.md) — mandatory bounded Context-of-Use contract
- [`measurement/qualification_record_schema.md`](measurement/qualification_record_schema.md) — documentation-level qualification-record contract

### Executable schema foundation
- [`schemas/v0.6.1/common/`](schemas/v0.6.1/common/) — development-stage Draft 2020-12 common scalar, hash, reference-base, repository-provenance, and actor-identity definitions with machine-readable valid and invalid test vectors
- [`schemas/v0.6.1/test_spec/`](schemas/v0.6.1/test_spec/) — first complete canonical-record schema, with lifecycle conditionals and machine-readable structural vectors

Local schema validation:

```text
python -m pip install -r requirements-schema-validation.txt
python tools/validate_schemas.py
python -m unittest discover -s tests -p "test_schema_validation.py"
```

The `Schema Validation` GitHub Actions workflow runs the harness and unit tests on pushes and pull requests.

### Supporting and historical documentation
- `docs/casef_one_pager.md` — one-page overview
- `measurement/artifact_taxonomy.md` — artifact vocabulary
- `measurement/log_schema.md` — superseded pre-canonical mixed log retained as historical material
- `measurement/conversation_audit_schema.md` — candidate conversation-audit payload for a future protocol-defined `rater_record`
- `redaction/guide.md` — redaction guidance
- `spec/model_registry.md` — model/platform registry
- `spec/prompt_registry.md` — prompt registry

### Current test assets
- `TC-L1-JSON-01`
- `TC-L1-COUNT-02`
- `TC-L3-AGENCY-01`

---

## Current v0.6.1 implementation boundary

CASEF v0.6.1 currently provides authoritative gate semantics, canonical contract documentation, documented canonical serialization rules, development-stage common schemas, and the first complete canonical-record schema: `test_spec`. A committed development harness and CI workflow validate all schemas and structural vectors.

CASEF does not yet provide serialized canonical record instances, the other five canonical record schemas, a canonical serializer, record or artifact hashing, an executable cross-record validator, a runner, an executable canonical qualification pipeline, a canonical evidence-generation workflow, or live qualification capability.

The contracts define which future records and evidence bindings are required. They do not provide the runner, owner-specific test validators, approved rater-protocol instances, executable human-assessment workflow, review workflow, or PI-approved gate rules still required before canonical evidence can be generated or qualification can be issued.

---

## What CASEF is not trying to prove

CASEF does **not** prove that a model is globally safe, aligned, or clinically valid.

It is narrower and more useful than that.

It helps answer questions like:

- Did the model violate an explicit constraint?
- Did it stay within its intended role?
- Did it abstain or escalate when required?
- Is the observed behavior documented in a reviewable form?
- Can another reviewer inspect the same artifact and reach the same conclusion?

---

## Intended users

CASEF is relevant for:

- clinical AI researchers
- evaluation engineers
- safety and reliability engineers
- high-stakes product teams
- QA / validation teams
- researchers building portable evidence-driven evaluation workflows

---

## Status

**Active development**

The v0.6.1 contract foundation currently establishes:

- authoritative qualification and gate semantics in `docs/gates.md`;
- canonical evidence ownership in `docs/canonical_evidence_contract.md`;
- executable development-stage common schemas plus the first complete canonical-record schema, `test_spec`, with machine-readable valid and invalid vectors;
- a committed dynamic schema-validation harness, unit tests, and a minimal structural-validation CI workflow;
- documentation-level contracts for all six canonical record types, including protocol-bound individual human assessment;
- a documentation-level rater-protocol contract; and
- documentation-level Context-of-Use and qualification-record contracts.

All six canonical record contracts are documented. The rater-protocol contract is documented, but no approved rater-protocol instance or executable human-assessment workflow exists.

No executable canonical qualification pipeline, canonical evidence pack, or current model qualification is provided yet.

---

## Design philosophy

CASEF starts from a simple premise:

> In high-stakes AI, generation is cheap.  
> Qualification is not.

The framework is designed to make failure visible, evidence portable, and evaluation decisions more defensible.

## Conversational Audit Layer

CASEF defines conversation audit as a future protocol-defined subtype of `rater_record`, focused on:
- uncertainty markers
- abstain / escalate trace
- operator accept / reject
- provenance / source trace
- final action trace

The current document lists candidate payload fields only. It is not a complete rater protocol, independent canonical record, replayable evidence example, or decision engine. Qualification semantics remain governed only by `docs/gates.md`.

See:
- `measurement/conversation_audit_schema.md`

---

## Recommended reading order

If you are opening the repository for the first time:

1. `docs/casef_one_pager.md`
2. [`docs/canonical_evidence_contract.md`](docs/canonical_evidence_contract.md)
3. [`docs/canonical_serialization_contract.md`](docs/canonical_serialization_contract.md)
4. [`schemas/v0.6.1/common/README.md`](schemas/v0.6.1/common/README.md)
5. [`spec/test_spec_contract.md`](spec/test_spec_contract.md)
6. [`spec/execution_manifest_contract.md`](spec/execution_manifest_contract.md)
7. [`measurement/run_record_schema.md`](measurement/run_record_schema.md)
8. [`measurement/validation_record_schema.md`](measurement/validation_record_schema.md)
9. [`spec/rater_protocol_contract.md`](spec/rater_protocol_contract.md)
10. [`measurement/rater_record_schema.md`](measurement/rater_record_schema.md)
11. [`spec/context_of_use.md`](spec/context_of_use.md)
12. [`docs/gates.md`](docs/gates.md)
13. [`measurement/qualification_record_schema.md`](measurement/qualification_record_schema.md)
14. selected test specifications and supporting vocabularies

---

## Practical use

CASEF is most useful when you need to answer:

- What exactly failed?
- Where is the evidence?
- How do we name it consistently?
- How do we compare runs across models and platforms?
- What should block a bounded use versus remain a documented limitation?

## License / use posture

Use CASEF as an evaluation and qualification framework.
Do not present it as medical advice, clinical decision support, or proof of deployment readiness without additional domain- and context-specific validation.

## License

This repository is released under the MIT License. See `LICENSE` for details.

---

## One-line summary

**CASEF is a physician-led framework for reproducible, artifact-based qualification of LLM behavior under explicit constraints.**
