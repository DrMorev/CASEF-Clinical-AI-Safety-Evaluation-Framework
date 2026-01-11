# CASEF demo_run (v0.2)

This folder is a minimal end-to-end evidence pack:
input prompt → raw model output → one JSONL log line per run.

## What this demo shows
- Level: L1 format/contract robustness
- Test: TC-L1-JSON-01 (single JSON object output)

## How to reproduce (manual)
1) Open a fresh chat/session on the target platform (no extra custom instructions if possible).
2) Copy-paste `inputs/TC-L1-JSON-01.txt` as the user message.
3) Save the model’s raw response exactly as-is into `outputs/<...>.txt`
   - No editing, no cleanup, no merging with logs.
4) Append one JSON line into `results/results.jsonl` describing that run.
5) Record context details in `run_manifest.md`.

## Notes
- This is NOT medical advice. It is an evaluation harness for format + safety posture in high-stakes communication.
- We do not claim internal telemetry; all artifacts are user-captured.
