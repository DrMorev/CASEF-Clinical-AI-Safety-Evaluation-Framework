# demo_run manifest

run_id: 2026-01-06_demo_01
operator: DrMorev
purpose: minimal evidence pack for CASEF (L1 JSON contract)

## Runs included
1) model: GPT-5.2 Thinking
   platform: ChatGPT
   session_type: fresh (YES/NO)
   extra_instructions: none / <describe>
   output_file: outputs/gpt-5.2-thinking__chatgpt__TC-L1-JSON-01.txt

2) model: Gemini 3 Flash
   platform: Google AI Studio
   session_type: fresh (YES/NO)
   extra_instructions: none / <describe>
   output_file: outputs/gemini-3-flash__aistudio__TC-L1-JSON-01.txt

3) model: Claude Opus 4.5
   platform: claude.ai
   session_type: fresh (YES/NO)
   extra_instructions: none / <describe>
   output_file: outputs/claude-opus-4.5__claudeai__TC-L1-JSON-01.txt

## Important confounds
- If a run was done inside a customized “doctor/scientist GPT”, mark it. It changes the system prompt and invalidates cross-model comparability unless explicitly studied.
