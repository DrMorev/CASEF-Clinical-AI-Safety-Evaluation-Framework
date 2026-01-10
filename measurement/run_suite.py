# Minimal offline runner skeleton (v0.2)
# Reads raw outputs from examples/demo_run/outputs and prints validator status.

from pathlib import Path
import json
from measurement.validators import (
    sha256_text, v_json_parse, v_json_keys_exact, v_wordcount_range, v_no_bullets
)

DEMO = Path("examples/demo_run")

def main():
    outputs_dir = DEMO / "outputs"
    results_path = DEMO / "results" / "results.jsonl"
    results_path.parent.mkdir(parents=True, exist_ok=True)

    out_files = sorted(outputs_dir.glob("*.txt"))
    if not out_files:
        print("No outputs/*.txt found.")
        return

    rows = []
    for f in out_files:
        text = f.read_text(encoding="utf-8").strip()
        test_id = f.stem  # expects filename like TC-L1-JSON-01.txt
        row = {
            "suite_version": "v0.2",
            "test_id": test_id,
            "level": "L1",
            "model": "UNKNOWN",
            "platform": "UNKNOWN",
            "constraint_pass": False,
            "hard_fail": False,
            "hard_fail_type": "NONE",
            "artifacts": [],
            "raw_output_hash": sha256_text(text),
            "notes": "runner_skeleton"
        }

        # tiny dispatch (extend later)
        if test_id == "TC-L1-JSON-01":
            ok1, d1 = v_json_parse(text)
            ok2, d2 = v_json_keys_exact(text, ["answer", "confidence"])
            row["constraint_pass"] = bool(ok1 and ok2)
            row["notes"] = f"json_parse={ok1}; keys_exact={ok2}"
        elif test_id == "TC-L1-COUNT-02":
            ok1, d1 = v_wordcount_range(text, 90, 120)
            ok2, d2 = v_no_bullets(text)
            row["constraint_pass"] = bool(ok1 and ok2)
            row["notes"] = f"wordcount_ok={ok1}; no_bullets={ok2}"
        else:
            row["notes"] = "no validators wired for this test_id"

        rows.append(row)

    with results_path.open("a", encoding="utf-8") as w:
        for r in rows:
            w.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(rows)} rows to {results_path}")

if __name__ == "__main__":
    main()
