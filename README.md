# CASEF — Clinical AI Safety Evaluation Framework

Physician-led, clinical-grade qualification framework for LLM safety & reliability: **spec → measurement → gates → evidence**.

This repo is **model-agnostic** and portable across platforms (apps/web/APIs). It focuses on reproducible evaluation artifacts, not internal telemetry.

## What’s in v0.1
- One-page overview: `docs/casef_one_pager.md`
- Minimal logging schema: `measurement/log_schema.md`
- Artifact taxonomy: `measurement/artifact_taxonomy.md`
- Redaction standard: `redaction/guide.md`
- Model/platform registry: `spec/model_registry.md`

## Quickstart (manual)
1) Pick a test prompt (or write one) and run it on a target platform/model.
2) Save the exact input/output (user-captured).
3) Record a JSONL line using `measurement/log_schema.md` and label artifacts using `measurement/artifact_taxonomy.md`.

## Non-goals
- No jailbreak content.
- No claims about internal model telemetry.
- Not medical advice; this is an evaluation framework.

## Status
Active development. Next: v0.2 adds initial test specs (Level 1–3) including an Agency & Stakes module.
