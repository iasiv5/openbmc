#!/usr/bin/env python3
import argparse
import datetime as dt
import re
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".github").exists() and (candidate / "README.md").exists():
            return candidate
    return start.parents[2]


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:64] if text else "lesson"


def next_lesson_id(entries_dir: Path, year: int) -> str:
    pattern = re.compile(rf"^LL-{year}-(\d{{3}})")
    max_n = 0
    if entries_dir.exists():
        for p in entries_dir.glob(f"LL-{year}-*.md"):
            m = pattern.match(p.stem)
            if m:
                max_n = max(max_n, int(m.group(1)))
    return f"LL-{year}-{max_n + 1:03d}"


def list_or_default(values, fallback):
    if values:
        return values
    return [fallback]


def render_frontmatter(data: dict) -> str:
    lines = ["---"]
    scalar_order = [
        "id",
        "title",
        "date",
        "component",
    ]
    for key in scalar_order:
        lines.append(f"{key}: {data[key]}")

    lines.append("tags: [" + ", ".join(data["tags"]) + "]")

    enum_order = [
        "topic",
        "failure_mode",
        "impact",
        "confidence",
        "sensitivity",
        "status",
        "owner",
        "applicability",
    ]
    for key in enum_order:
        lines.append(f"{key}: {data[key]}")

    if data["template"] == "deep":
        lines.append("lifecycle: [detect, diagnose, fix, verify, prevent]")

    for field in ["symptoms", "root_cause", "fix", "prevention", "links"]:
        lines.append(f"{field}:")
        for item in data[field]:
            lines.append(f"  - {item}")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def render_body(template: str) -> str:
    if template == "deep":
        return (
            "## Context\n\n"
            "Describe environment, versions, machine, and constraints.\n\n"
            "## Detection and impact\n\n"
            "- First observed in:\n"
            "- User/business impact:\n"
            "- Scope of affected systems:\n\n"
            "## Investigation timeline\n\n"
            "1. Hypothesis A and result\n"
            "2. Hypothesis B and result\n"
            "3. Confirmed root cause\n\n"
            "## Final fix\n\n"
            "Describe exact changes and why they are safe.\n\n"
            "## Validation\n\n"
            "- Build/runtime/tests performed\n"
            "- Negative tests\n\n"
            "## Prevention plan\n\n"
            "- Process guardrails\n"
            "- Tooling checks\n"
            "- Ownership and follow-up date\n"
        )

    return (
        "## Summary\n\n"
        "One-paragraph summary of what happened and why this lesson matters.\n\n"
        "## Verification\n\n"
        "- Evidence 1:\n"
        "- Evidence 2:\n\n"
        "## Reuse notes\n\n"
        "- When to apply:\n"
        "- When not to apply:\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a lesson entry with auto ID")
    parser.add_argument("--type", choices=["quick", "deep"], default="quick")
    parser.add_argument("--title", required=True)
    parser.add_argument("--component", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--applicability", required=True)
    parser.add_argument("--topic", default="build")
    parser.add_argument("--failure-mode", default="config-drift")
    parser.add_argument("--impact", default="medium")
    parser.add_argument("--confidence", default="validated")
    parser.add_argument("--sensitivity", default="internal")
    parser.add_argument("--status", default="draft")
    parser.add_argument("--tag", action="append", dest="tags")
    parser.add_argument("--symptom", action="append", dest="symptoms")
    parser.add_argument("--root-cause", action="append", dest="root_causes")
    parser.add_argument("--fix", action="append", dest="fixes")
    parser.add_argument("--prevention", action="append", dest="preventions")
    parser.add_argument("--link", action="append", dest="links")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve())
    entries_dir = repo_root / "docs" / "lessons" / "entries"
    entries_dir.mkdir(parents=True, exist_ok=True)

    year = int(args.date[:4])
    lesson_id = next_lesson_id(entries_dir, year)
    slug = slugify(args.title)
    filename = f"{lesson_id}-{slug}.md"
    out_path = entries_dir / filename

    data = {
        "template": args.type,
        "id": lesson_id,
        "title": args.title,
        "date": args.date,
        "component": args.component,
        "tags": args.tags if args.tags else ["lesson", "bugfix", "knowledge"],
        "topic": args.topic,
        "failure_mode": args.failure_mode,
        "impact": args.impact,
        "confidence": args.confidence,
        "sensitivity": args.sensitivity,
        "status": args.status,
        "owner": args.owner,
        "applicability": args.applicability,
        "symptoms": list_or_default(args.symptoms, "TODO: add symptom"),
        "root_cause": list_or_default(args.root_causes, "TODO: add root cause"),
        "fix": list_or_default(args.fixes, "TODO: add fix action"),
        "prevention": list_or_default(args.preventions, "TODO: add prevention action"),
        "links": list_or_default(args.links, "docs/lessons/README.md"),
    }

    content = render_frontmatter(data) + render_body(args.type)

    if args.dry_run:
        print(out_path.relative_to(repo_root))
        return 0

    out_path.write_text(content, encoding="utf-8")
    print(out_path.relative_to(repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
