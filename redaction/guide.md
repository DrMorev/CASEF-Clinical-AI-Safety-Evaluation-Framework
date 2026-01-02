# CASEF Redaction Guide (v0.1)

Goal: enable publishing evaluation evidence without leaking personal data, proprietary information, or misleading "telemetry" claims.

This repo stores **user-captured** prompts and model outputs. It does not contain internal platform logs.

---

## Non-negotiable labels
When publishing any captured interaction, add one of these headers:

- "MODEL-GENERATED CONTENT (USER-CAPTURED). NOT PLATFORM TELEMETRY."
- "SANITIZED EXAMPLE. REPRODUCIBLE PROMPT/OUTPUT RECORD."

---

## What must be removed (always)
- Personal identifiers: names, addresses, phone numbers, emails, account IDs
- Legal case numbers, medical record numbers
- Exact locations more specific than city/province (unless explicitly necessary and safe)
- Payment details, order numbers, tracking numbers
- Private links (signed URLs), API keys, tokens, secrets
- Any third-party private content not owned by you

---

## What should be generalized (usually)
- Employer names → "employer"
- Exact dates/times → month-level unless timing matters experimentally
- Specific clinic/hospital identifiers → "clinical setting"
- Unnecessary unique phrases that could re-identify a person

---

## Safe replacements (examples)
- "<EMAIL>" "<PHONE>" "<ADDRESS>" "<ID>"
- "<PATIENT_AGE_RANGE>" instead of exact age
- "<DATE_YYYY-MM>" instead of full date
- "<COMPANY>" "<CITY_PROVINCE>"

---

## Evidence structure (recommended)
If you include examples in /evidence:
- Always include a short "Context" paragraph (sanitized)
- Include the exact prompt + exact output (sanitized)
- Include evaluation fields (constraint_pass, hard_fail, artifact_types, notes)
- Avoid publishing long chat histories; prefer minimal reproductions

---

## Provenance rule
For every published artifact, you must be able to answer:
1) Who created this prompt? (you)
2) Is the output model-generated? (yes)
3) Can someone reproduce it with the same prompt on a similar platform? (best-effort)

---

## What CASEF does NOT do
- No jailbreak instructions
- No instructions to bypass platform safeguards
- No claims that results represent internal model behavior beyond the observed output
