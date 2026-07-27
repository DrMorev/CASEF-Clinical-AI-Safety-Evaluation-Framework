# Diagnostic capture spike protocol

**NON-CANONICAL**

**EXPERIMENTAL**

**PRE-REGISTERED BEFORE IMPLEMENTATION**

**NOT EVIDENCE**

**NOT QUALIFICATION**

## 1. Purpose and question

This protocol freezes the question and fixture corpus for a future, bounded implementation spike. It is not a canonical CASEF contract, evidence record, execution record, validation record, or qualification artifact.

The future spike asks:

> Can CASEF ingest arbitrary bounded source files as exact bytes, calculate SHA-256 over the stored source bytes before any decoding or transformation, and emit explicit diagnostic receipts without conflating source artifacts, derivative artifacts, execution status, capture status, evidence eligibility, or qualification?

The fixtures and expected byte identities are fixed in [`fixtures/manifest.json`](fixtures/manifest.json). The manifest is experimental metadata only.

## 2. Boundary and terminology

| Item | Bounded meaning in this spike | Not permitted to mean |
|---|---|---|
| Source artifact | Exact fixture bytes read from the frozen fixture path before decoding or transformation | A transformed, normalized, decoded, redacted, or rendered substitute |
| Derivative artifact | Separately identified bytes created only by an explicit transformation attempt | A silent replacement for the source artifact |
| Diagnostic receipt | A non-canonical implementation output reporting source path, observed byte length, observed hash, and transformation status | Evidence, a canonical record, a finding, gate result, qualification, or permission |
| Execution status | Future bounded implementation-process state | Capture status, source-byte integrity, evidence eligibility, or model behavior |
| Capture status | Future observation of whether source bytes were read and reported | Execution status, evidence eligibility, qualification, or use permission |

No diagnostic receipt may masquerade as a canonical evidence record. No result of this spike may claim evidence eligibility, gate success, qualification, clinical validity, deployment readiness, or use permission.

## 3. Frozen fixture procedure

Before a future spike run, the implementation must:

1. identify the frozen commit and fixture path;
2. read every fixture in binary mode;
3. compare observed source-byte length and SHA-256 with the manifest before decoding or transformation;
4. preserve the source bytes unchanged throughout the diagnostic path; and
5. treat any fixture mismatch as experiment invalidation, not as a model or safety observation.

The implementation may attempt a separately reported transformation only after source-byte hashing. A failed transformation must not mutate, overwrite, or replace the source artifact.

## 4. Expected observations

The future implementation is expected to show all of the following:

- every fixture is read in binary mode;
- observed byte length equals the manifest value;
- observed SHA-256 equals the manifest value;
- BOM bytes remain present;
- CRLF and LF remain distinguishable;
- trailing whitespace remains present;
- invalid UTF-8 does not prevent source-byte hashing;
- no decoding occurs before source hashing;
- no derivative artifact is created unless a transformation is explicitly attempted;
- a failed transformation does not mutate or replace the source artifact; and
- each diagnostic receipt identifies source path, observed length, observed hash, and transformation status.

These are engineering observations only. A match does not establish evidence eligibility or any qualification result.

## 5. Ordinary implementation defects

The following are ordinary implementation defects, not architecture failures:

- wrong file path;
- coding error in SHA-256 calculation;
- accidental text-mode file opening;
- missing fixture iteration;
- malformed diagnostic formatting;
- incorrect expected value copied into implementation; and
- an unhandled exception where this protocol already defines the correct behavior.

An ordinary defect requires correction and a rerun. It does not support an architectural conclusion.

## 6. Architecture-review triggers

Architecture review is required if making the spike work would require any of the following:

1. source provenance must be discarded or overwritten;
2. the same fact requires incompatible ownership in multiple canonical record types;
3. one execution attempt cannot be represented without an undocumented transformation;
4. execution status and capture status must be collapsed into one axis;
5. a necessary fact has no defined future owner;
6. source and derivative bytes cannot be distinguished;
7. two independent compliant implementations necessarily produce incompatible representations;
8. correct hashing requires decoding, newline normalization, BOM removal, Unicode repair, trimming, or other content mutation;
9. diagnostic receipts would need to masquerade as canonical evidence records; or
10. the spike can succeed only by claiming evidence eligibility, gate success, qualification, or use permission.

## 7. Experiment invalidation conditions

The result is invalid if:

- any fixture changes after protocol freeze;
- implementation begins before the protocol/fixture commit is accepted;
- manifest values are edited after observing implementation results;
- source files are generated dynamically during the execution run;
- the implementation hashes a transformed buffer rather than the committed source bytes;
- not all committed fixtures are executed;
- environment or tool behavior cannot be reconstructed;
- output records are manually edited before review; or
- a fixture's working-tree bytes do not match the frozen manifest before the spike begins.

## 8. No-conclusion conditions

No architectural conclusion may be drawn if:

- the implementation fails for an ordinary coding reason;
- independent hash verification is absent;
- only text-valid fixtures are exercised;
- binary or invalid-Unicode fixtures are skipped;
- platform-specific behavior is observed on only one environment;
- diagnostic receipts are incomplete; or
- fixture identity cannot be verified against the frozen commit.

## 9. Current boundary

Task 02N-A performs no capture implementation or execution. It creates neither a reusable hashing utility nor a production reader, parser, runner, artifact record, schema, validator, model/API call, generated evidence, gate execution, or qualification action.
