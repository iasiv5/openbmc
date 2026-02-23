#!/usr/bin/env python3
import argparse
import json
import shlex
import subprocess
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".github").exists() and (candidate / "README.md").exists():
            return candidate
    return start.parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Bridge sentinel detection to next archival actions")
    parser.add_argument("--log", help="Path to log file")
    parser.add_argument("--text", help="Inline text to analyze")
    parser.add_argument("--had-failure", action="store_true", help="Mark that this cycle previously failed")
    parser.add_argument("--title", default="<lesson-title>", help="Suggested lesson title")
    parser.add_argument("--component", default="<component>", help="Suggested component")
    parser.add_argument("--owner", default="<owner>", help="Suggested owner")
    parser.add_argument("--applicability", default="<applicability>", help="Suggested applicability")
    parser.add_argument("--type", choices=["quick", "deep"], default="quick", help="Lesson template type")
    parser.add_argument("--no-execute", action="store_true", help="Only output next actions without creating or archiving")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve())
    detector = repo_root / ".github" / "skills" / "fix-complete-sentinel" / "scripts" / "detect_fix_complete.py"

    if not detector.exists():
        print(json.dumps({"ready": False, "reason": "detector script not found"}, ensure_ascii=False))
        return 2

    cmd = ["python3", str(detector)]
    if args.log:
        cmd += ["--log", args.log]
    if args.text:
        cmd += ["--text", args.text]
    if args.had_failure:
        cmd += ["--had-failure"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(json.dumps({"ready": False, "reason": "detector execution failed", "stderr": result.stderr.strip()}, ensure_ascii=False))
        return result.returncode

    try:
        detection = json.loads(result.stdout.strip() or "{}")
    except json.JSONDecodeError:
        print(json.dumps({"ready": False, "reason": "invalid detector output", "raw": result.stdout.strip()}, ensure_ascii=False))
        return 2

    ready = bool(detection.get("ready", False))

    create_cmd = [
        "python3",
        ".github/skills/lesson-archiver/scripts/create_lesson.py",
        "--type",
        args.type,
        "--title",
        args.title,
        "--component",
        args.component,
        "--owner",
        args.owner,
        "--applicability",
        args.applicability,
    ]

    archive_prefix = [
        ".github/skills/lesson-archiver/scripts/archive-after-fix.sh",
    ]

    executed = False
    created_entry = ""
    archive_stdout = ""
    archive_stderr = ""

    if ready and not args.no_execute:
        if any(v.startswith("<") and v.endswith(">") for v in [args.title, args.component, args.owner, args.applicability]):
            print(
                json.dumps(
                    {
                        "ready": True,
                        "reason": "missing required lesson metadata for auto-execution",
                        "required": ["--title", "--component", "--owner", "--applicability"],
                    },
                    ensure_ascii=False,
                )
            )
            return 2

        create_result = subprocess.run(create_cmd, capture_output=True, text=True, cwd=repo_root)
        if create_result.returncode != 0:
            print(
                json.dumps(
                    {
                        "ready": True,
                        "executed": False,
                        "reason": "create lesson failed",
                        "stderr": create_result.stderr.strip(),
                    },
                    ensure_ascii=False,
                )
            )
            return create_result.returncode

        created_entry = create_result.stdout.strip().splitlines()[-1].strip()
        archive_cmd = [*archive_prefix, created_entry]
        archive_result = subprocess.run(archive_cmd, capture_output=True, text=True, cwd=repo_root)
        executed = archive_result.returncode == 0
        archive_stdout = archive_result.stdout.strip()
        archive_stderr = archive_result.stderr.strip()

        if archive_result.returncode != 0:
            print(
                json.dumps(
                    {
                        "ready": True,
                        "executed": False,
                        "reason": "archive flow failed",
                        "created_entry": created_entry,
                        "stdout": archive_stdout,
                        "stderr": archive_stderr,
                    },
                    ensure_ascii=False,
                )
            )
            return archive_result.returncode

    response = {
        "ready": ready,
        "ask": "要不要归档这次经验？" if (ready and args.no_execute) else "",
        "reason": detection.get("reason", ""),
        "executed": executed,
        "created_entry": created_entry,
        "archive_stdout": archive_stdout,
        "archive_stderr": archive_stderr,
        "next": {
            "create_lesson_cmd": " ".join(shlex.quote(x) for x in create_cmd),
            "archive_cmd_template": ".github/skills/lesson-archiver/scripts/archive-after-fix.sh docs/lessons/entries/<new-file>.md",
        },
    }

    print(json.dumps(response, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
