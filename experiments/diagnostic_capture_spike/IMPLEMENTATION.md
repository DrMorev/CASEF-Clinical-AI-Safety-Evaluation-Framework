# Diagnostic capture spike implementation

**NON-CANONICAL EXPERIMENTAL IMPLEMENTATION**

This is the bounded Task 02N-B implementation of the frozen diagnostic-capture
spike. It is not a production CLI, runner, capture platform, artifact store,
validator, evidence generator, or qualification mechanism.

## Frozen input

The official input commit is `75a580d8057b483fa76cedcc2e773e2144016a96`.
The protocol, manifest, and fixtures are materialized outside the working tree
from that commit. The run first checks every input's exact stored bytes against
the frozen manifest; a mismatch invalidates the experiment.

The official materialization method is:

```text
git -c core.autocrlf=false archive 75a580d8057b483fa76cedcc2e773e2144016a96 \
  experiments/diagnostic_capture_spike/PROTOCOL.md \
  experiments/diagnostic_capture_spike/fixtures | tar -x -C <FROZEN_ROOT>
```

Disabling Git text filtering for this export is required so the materialized
files are the raw frozen commit bytes rather than platform-adjusted text.

## Two phases

1. Read all source fixtures in binary mode, calculate SHA-256 directly over
   those returned bytes, and compare length and digest with the manifest.
2. Only if every identity check passes, attempt strict UTF-8 decoding in memory.
   Decode success or `UnicodeDecodeError` is recorded separately from source
   capture status. No decoded or derivative byte artifact is written.

## Command

After exporting the frozen source tree to `<FROZEN_ROOT>`, run:

```text
python experiments/diagnostic_capture_spike/run_capture_spike.py \
  --source-root <FROZEN_ROOT> \
  --manifest <FROZEN_ROOT>/experiments/diagnostic_capture_spike/fixtures/manifest.json \
  --frozen-input-commit 75a580d8057b483fa76cedcc2e773e2144016a96 \
  --implementation-commit <IMPLEMENTATION_COMMIT> \
  --output-directory experiments/diagnostic_capture_spike/results
```

Exit codes are `0` for the successful bounded experiment, `1` for command or
configuration error, `2` for manifest/source-identity invalidation, and `3` for
an unexpected implementation or execution failure.

## Outputs and limits

Each receipt contains exact expected and observed source identity, separate
capture and transformation status, and whether a derivative artifact was
created. It has no timestamp, absolute path, user, host, machine ID, or
qualification field. `run_summary.json` reports only bounded mechanical counts.

This spike cannot establish scientific validity, evidence eligibility, model
safety, gate success, qualification, clinical readiness, or use permission.
