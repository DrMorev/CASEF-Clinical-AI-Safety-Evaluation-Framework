# Prompt Registry (v0.2)

Canon rule: every test has a stable test_id and a file path.

## Level 1 (Format/Constraints)
- test_id: TC-L1-JSON-01
  path: spec/tests/level1/TC-L1-JSON-01.md
  validator: V_JSON_PARSE
  gate: default PASS/FAIL (docs/gates.md)

- test_id: TC-L1-COUNT-02
  path: spec/tests/level1/TC-L1-COUNT-02.md
  validator: V_WORDCOUNT
  gate: default PASS/FAIL (docs/gates.md)

## Level 3 (Agency & Stakes)
- test_id: TC-L3-AGENCY-01
  path: framework/level3/agency/TC-L3-AGENCY-01.md
  validator: V_JSON_PARSE (if strict JSON required) + format checks
  gate: default PASS/FAIL + hard_fail rules (inside test)
