# CASEF Model & Platform Registry (v0.1)

Purpose: record which model/platform combos were evaluated, without baking model names into the framework.

This is a living index. Entries should be factual and time-stamped.

---

## Fields (per entry)
- registry_id: short ID (e.g., "GPT-CHAT-2026-01")
- date_utc_first_seen: ISO-8601
- platform: e.g., chatgpt_web / openai_api / gemini_web / anthropic_api
- model_reported: exact string shown by UI/API (or null)
- reasoning_mode: if shown (thinking/reasoning/standard) else null
- preset: if shown else null
- notes: anything relevant (e.g., "model id hidden", "UI changed label")

---

## Entries

### Example
- registry_id: GPT-CHAT-2026-01
  date_utc_first_seen: 2026-01-01T00:00:00Z
  platform: chatgpt_web
  model_reported: gpt-5.2
  reasoning_mode: thinking
  preset: default
  notes: ""

(Add your real entries below as you run tests.)
