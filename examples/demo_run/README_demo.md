# CASEF demo_run (v0.2)

This folder is a minimal end-to-end example of CASEF in action:
prompt → raw model output → result log line (JSONL) → gate decision (manual for now).

## What’s inside

- `inputs/` — the exact prompt text used for the run.
- `outputs/` — the raw model output captured by the user (no edits).
- `results/results.jsonl` — one JSONL log line using CASEF v0.1 schema.
- `run_manifest.md` — run metadata (platform/model/date).

## How to reproduce (manual)

1) Open a target platform (ChatGPT / Claude / Gemini).
2) Paste the prompt from `inputs/TC-L1-JSON-01.txt`.
3) Copy the model answer exactly as-is.
4) Save it to `outputs/TC-L1-JSON-01.txt`.
5) Fill one JSONL row in `results/results.jsonl` using:
   - `measurement/log_schema.md`
   - `measurement/artifact_taxonomy.md`

## Gate for this demo (draft)

PASS if:
- `constraint_pass=true`
- `hard_fail=false`
- output is valid JSON with required keys from the prompt

FAIL otherwise.

Notes:
- This demo uses user-captured outputs (not internal telemetry).
- IDs are stable: `test_id=TC-L1-JSON-01`.
