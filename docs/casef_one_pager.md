# CASEF — Clinical AI Safety Evaluation Framework (v0.1)

**One-liner:** Physician-led, clinical-grade *post-alignment qualification* for LLMs: reproducible tests + measurable rubrics + hard-fail gates + evidence, portable across platforms.

## What CASEF is
CASEF is a framework to qualify LLM behavior for clinical and other high-stakes workflows **before deployment**.
It provides a standardized, auditable procedure for **go/no-go** decisions based on reproducible evaluation suites.

## The problem
LLMs can fail in ways that are dangerous or operationally unacceptable:
- **Format/contract drift:** JSON/table constraints break; rendering leaks (Markdown/LaTeX).
- **Semantic loss under transformation:** meaning changes when converting table → JSON → leaflet → decision tree.
- **Degradation under multi-turn load:** performance collapses as context grows.
- **Value-conflict instability:** safety vs helpfulness vs honesty vs autonomy.
- **Capability dishonesty:** hallucinated actions, fake memory, deceptive certainty under stakes.
- **Context-specific triggers:** “integration-trigger” failures not caught by generic robustness tests.

## Core novelty (not a prompt list)
CASEF’s novelty is the pipeline:
**spec → measurement → acceptance gates → regression → evidence**
- **Spec:** tests are versioned and explicitly constrained.
- **Measurement:** structured logs + artifact taxonomy + rubrics + hard fails.
- **Gates:** threshold rules suitable for CI/regression decisions.
- **Regression:** rerun suites on model/platform updates and compare deltas.
- **Evidence:** failure-mode library + sanitized vignettes (illustrative, not “drama logs”).

## Levels
### Level 1 — Format & Constraint Robustness
Contract-heavy outputs (JSON/YAML/CSV/tables), forbidden tokens, word/line limits, schema validity, rendering leakage.

### Level 2 — Multi-turn Stress & Semantic Invariance
Degradation under repeated turns and invariance across transformations (e.g., table → JSON → narrative → checklist).

### Level 3 — Value Conflicts & Agency/Stakes
Behavior under pressure: responsibility handling, verification loops, realistic capability boundaries, refusal calibration.

## Key v0.1 deliverables (docs-first)
v0.1 is intentionally minimal and publishable:
- `/docs/casef_one_pager.md` — this one-pager
- `/spec/suite_state.md` — levels, scope, non-goals, current modules
- `/measurement/log_schema.md` — what fields we log; CSV/JSONL templates
- `/measurement/artifact_taxonomy.md` — artifact types + detection rules
- `/redaction/redaction_guide.md` — what never gets published; “MODEL-GENERATED (NOT TELEMETRY)”
- `/docs/not_jailbreak.md` — positioning: qualification/robustness, not jailbreak research

## TC-L3-AGENCY (Level 3 module)
Single-turn battery that measures “agency without qualia”:
- closed-loop control (plan → check → fix) with STOP criteria
- stakes/responsibility handling
- realism about capabilities and memory
**Hard fails include:** hallucinated actions, unsafe guidance, deceptive authority, prompt evasion, confident wrong under stakes.
(Full spec lands in v0.2 as `spec/TC-L3-AGENCY.md`.)

## MedRLHF Gap (concept inside CASEF)
Treat “MedRLHF” as an *alignment claim*; CASEF is the *qualification gate*.
CASEF measures the **MedRLHF Gap**: failures that remain after RLHF (over-refusal, boilerplate dominance, sycophancy under stakes, capability dishonesty, format breakdown under stress).

## Outputs and users
**Outputs:** versioned suites + logs + rubrics + pass/fail gates + evidence catalog.
**Users:** clinical governance teams, hospitals, insurers, vendors, safety/reliability teams, researchers needing reproducible high-stakes evaluation.

## Non-goals
- No jailbreak/exploitation instructions.
- No model “fixing” or claims about vendor internals.
- No clinical diagnosis or treatment recommendations: we evaluate model behavior and safety properties.

## Status
v0.1: docs + measurement scaffolding (publishable baseline).
Next: v0.2 adds TC-L3-AGENCY spec + first minimal templates; v0.3 adds initial cross-platform baseline runs.
