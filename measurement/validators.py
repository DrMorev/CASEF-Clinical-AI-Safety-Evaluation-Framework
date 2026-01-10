import json
import re
import hashlib
from typing import Dict, Any, List, Tuple

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def v_json_parse(text: str) -> Tuple[bool, Dict[str, Any]]:
    try:
        obj = json.loads(text)
        return True, {"parsed_type": type(obj).__name__}
    except Exception as e:
        return False, {"error": str(e)}

def v_json_keys_exact(text: str, keys: List[str]) -> Tuple[bool, Dict[str, Any]]:
    ok, details = v_json_parse(text)
    if not ok:
        return False, details
    obj = json.loads(text)
    if not isinstance(obj, dict):
        return False, {"error": "not a JSON object"}
    got = sorted(list(obj.keys()))
    exp = sorted(keys)
    return got == exp, {"expected": exp, "got": got}

def wordcount(s: str) -> int:
    return len(re.findall(r"\b\w+\b", s))

def v_wordcount_range(text: str, lo: int, hi: int) -> Tuple[bool, Dict[str, Any]]:
    wc = wordcount(text)
    return (lo <= wc <= hi), {"wordcount": wc, "range": [lo, hi]}

def v_no_bullets(text: str) -> Tuple[bool, Dict[str, Any]]:
    has_bullets = bool(re.search(r"(^|\n)\s*[-*•]\s+", text))
    return (not has_bullets), {"has_bullets": has_bullets}
