#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

SUCCESS_PATTERNS = [
    re.compile(r"exit\s+code[:=]?\s*0", re.IGNORECASE),
    re.compile(r"all succeeded", re.IGNORECASE),
    re.compile(r"tasks summary:.*all succeeded", re.IGNORECASE),
    re.compile(r"build.*succeeded", re.IGNORECASE),
    re.compile(r"passed", re.IGNORECASE),
    re.compile(r"verified", re.IGNORECASE),
    re.compile(r"resolved", re.IGNORECASE),
]

FAIL_PATTERNS = [
    re.compile(r"\berror\b", re.IGNORECASE),
    re.compile(r"failed", re.IGNORECASE),
    re.compile(r"non-zero exit code", re.IGNORECASE),
    re.compile(r"exit\s+code[:=]?\s*[1-9]\d*", re.IGNORECASE),
]


def analyze(text: str, had_failure: bool):
    success_hits = [p.pattern for p in SUCCESS_PATTERNS if p.search(text)]
    fail_hits = [p.pattern for p in FAIL_PATTERNS if p.search(text)]

    strong_signal = bool(success_hits) and (had_failure or bool(fail_hits))
    medium_signal = bool(success_hits) and not strong_signal

    ready = strong_signal
    reason = ""
    if ready:
        reason = "detected success transition after failure context"
    elif medium_signal:
        reason = "success signal found but missing failure context"
    else:
        reason = "no reliable completion signal"

    return {
        "ready": ready,
        "ask": "要不要归档这次经验？" if ready else "",
        "reason": reason,
        "success_signals": len(success_hits),
        "failure_signals": len(fail_hits),
        "had_failure_context": had_failure,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect if fix is complete and archival prompt should be asked")
    parser.add_argument("--log", help="Path to log file")
    parser.add_argument("--text", help="Inline text to analyze")
    parser.add_argument("--had-failure", action="store_true", help="Mark that this cycle previously failed")
    args = parser.parse_args()

    if not args.log and not args.text:
        print(json.dumps({"ready": False, "reason": "no input"}, ensure_ascii=False))
        return 2

    content = ""
    if args.log:
        path = Path(args.log)
        if not path.exists():
            print(json.dumps({"ready": False, "reason": f"log not found: {args.log}"}, ensure_ascii=False))
            return 2
        content += path.read_text(encoding="utf-8", errors="ignore")

    if args.text:
        if content:
            content += "\n"
        content += args.text

    result = analyze(content, args.had_failure)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
