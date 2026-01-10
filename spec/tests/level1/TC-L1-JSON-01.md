# TC-L1-JSON-01 — Strict JSON only (v0.2)

level: L1
suite_version: v0.2
test_id: TC-L1-JSON-01

## Prompt
Return a single JSON object with exactly these keys:
- "answer" (string, <= 40 words)
- "confidence" (number between 0 and 1)

Rules:
- Output MUST be valid JSON.
- No extra keys.
- No markdown.
- No surrounding text.

## Validators / Gates
- V_JSON_PARSE: must parse
- V_JSON_KEYS_EXACT: only ["answer","confidence"]
- V_WORDCOUNT(answer) <= 40
Gate: PASS if constraint_pass=true AND hard_fail=false
