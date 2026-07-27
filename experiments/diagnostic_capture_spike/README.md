# CASEF diagnostic capture spike

This directory pre-registers a bounded diagnostic capture spike before any capture implementation exists. Task 02M established the first schema-validation foundation; it did not create capture behavior, a runner, source-artifact storage, or a diagnostic capture path.

The fixture corpus is frozen before implementation. Each file is defined by explicit bytes, with its expected byte length and SHA-256 recorded in [`fixtures/manifest.json`](fixtures/manifest.json). A future implementation must verify the committed fixture bytes before interpreting any result.

## Artifact boundary

- **Source bytes** are the exact committed fixture bytes read before decoding, transformation, or normalization.
- **Derivative bytes** may exist only after an explicitly attempted and separately identified transformation; they never replace source bytes.
- **Diagnostic receipts** are bounded implementation outputs that report observations such as path, byte length, hash, and transformation status. They are not canonical records or evidence.

No file in this directory is canonical qualification evidence. This pre-registration creates no gate result, severity, qualification outcome, policy consequence, or use permission.

The future capture implementation belongs to a separate Task 02N-B. This task makes no model or API call, creates no runner, performs no schema migration, and takes no qualification action.
