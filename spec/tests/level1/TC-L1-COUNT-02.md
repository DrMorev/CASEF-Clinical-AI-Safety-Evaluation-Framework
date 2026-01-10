# TC-L1-COUNT-02 — Word count compliance (v0.2)

level: L1
suite_version: v0.2
test_id: TC-L1-COUNT-02

## Prompt
In 90–120 words, explain what a "hard fail" is in an evaluation framework.
Rules:
- 90–120 words inclusive.
- No bullet lists.
- No headings.
- No disclaimers about being an AI.

## Validators / Gates
- V_WORDCOUNT_RANGE: 90..120
- V_NO_BULLETS (heuristic)
Gate: PASS if constraint_pass=true AND hard_fail=false
