#!/usr/bin/env python3
import datetime as dt
import os
import re
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".github").exists() and (candidate / "README.md").exists():
            return candidate
    return start.parents[2]


ROOT = find_repo_root(Path(__file__).resolve())
LESSONS_DIR = ROOT / "docs" / "lessons" / "entries"

TOPIC_VALUES = {
    "build", "boot", "kernel", "device-tree", "packaging", "security", "ci", "tooling"
}
FAILURE_MODE_VALUES = {
    "config-drift", "size-overflow", "dependency-missing", "provider-conflict", "regression", "flaky"
}
IMPACT_VALUES = {"low", "medium", "high", "critical"}
CONFIDENCE_VALUES = {"hypothesis", "validated"}
SENSITIVITY_VALUES = {"public", "internal", "confidential"}
STATUS_VALUES = {"draft", "active", "superseded", "archived"}
LIFECYCLE_VALUES = {"detect", "diagnose", "fix", "verify", "prevent"}

SECRET_PATTERNS = [
    re.compile(r"(?i)password\s*[:=]\s*\S+"),
    re.compile(r"(?i)token\s*[:=]\s*\S+"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*\S+"),
    re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH|DSA) PRIVATE KEY-----"),
]

ID_RE = re.compile(r"^LL-\d{4}-\d{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^(https?://\S+|[A-Za-z0-9_./-]+)$")


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, "missing frontmatter start '---'"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "missing frontmatter end '---'"
    block = text[4:end]
    body = text[end + 5 :]
    data = parse_simple_yaml(block)
    return (data, body), None


def parse_simple_yaml(block: str):
    data = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.strip().startswith("#"):
            i += 1
            continue
        if raw.startswith("  - "):
            i += 1
            continue
        if ":" not in raw:
            i += 1
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            arr = []
            i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                arr.append(lines[i][4:].strip())
                i += 1
            data[key] = arr
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if inner:
                data[key] = [v.strip().strip('"\'') for v in inner.split(",")]
            else:
                data[key] = []
        else:
            data[key] = value.strip('"\'')
        i += 1
    return data


def err(errors, path, msg):
    errors.append(f"ERROR {path}: {msg}")


def warn(warnings, path, msg):
    warnings.append(f"WARN  {path}: {msg}")


def validate_date(date_str: str):
    if not DATE_RE.match(date_str):
        return False
    try:
        dt.date.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def ensure_list(data, key):
    val = data.get(key)
    return isinstance(val, list) and len(val) > 0


def validate_file(path: Path, seen_ids, errors, warnings):
    text = path.read_text(encoding="utf-8")
    parsed, parse_err = parse_frontmatter(text)
    rel = path.relative_to(ROOT)
    if parse_err:
        err(errors, rel, parse_err)
        return
    data, body = parsed

    required = [
        "id", "title", "date", "component", "tags", "topic", "failure_mode", "impact",
        "confidence", "sensitivity", "status", "owner", "applicability", "symptoms",
        "root_cause", "fix", "prevention", "links",
    ]

    for k in required:
        if k not in data:
            err(errors, rel, f"missing required field '{k}'")

    lesson_id = data.get("id", "")
    if lesson_id:
        if not ID_RE.match(lesson_id):
            err(errors, rel, "id must match LL-YYYY-NNN")
        elif lesson_id in seen_ids:
            err(errors, rel, f"duplicate id '{lesson_id}'")
        else:
            seen_ids.add(lesson_id)

    title = data.get("title", "")
    if title and len(title) > 120:
        warn(warnings, rel, "title longer than 120 characters")

    date = data.get("date", "")
    if date and not validate_date(date):
        err(errors, rel, "date must be valid ISO YYYY-MM-DD")

    tags = data.get("tags")
    if isinstance(tags, list):
        if not (3 <= len(tags) <= 8):
            warn(warnings, rel, "tags should contain 3-8 items")
    else:
        err(errors, rel, "tags must be a list")

    enum_checks = [
        ("topic", TOPIC_VALUES),
        ("failure_mode", FAILURE_MODE_VALUES),
        ("impact", IMPACT_VALUES),
        ("confidence", CONFIDENCE_VALUES),
        ("sensitivity", SENSITIVITY_VALUES),
        ("status", STATUS_VALUES),
    ]
    for key, allowed in enum_checks:
        value = data.get(key)
        if value and value not in allowed:
            err(errors, rel, f"{key} must be one of: {', '.join(sorted(allowed))}")

    lifecycle = data.get("lifecycle")
    if lifecycle is not None:
        if not isinstance(lifecycle, list):
            err(errors, rel, "lifecycle must be a list")
        else:
            invalid = [v for v in lifecycle if v not in LIFECYCLE_VALUES]
            if invalid:
                err(errors, rel, f"lifecycle contains invalid values: {invalid}")

    for list_key in ["symptoms", "root_cause", "fix", "prevention", "links"]:
        if list_key in data and not ensure_list(data, list_key):
            err(errors, rel, f"{list_key} must be a non-empty list")

    links = data.get("links", [])
    if isinstance(links, list):
        for link in links:
            if not URL_RE.match(str(link)):
                warn(warnings, rel, f"link looks malformed: {link}")

    content = f"{text}\n{body}"
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            err(errors, rel, "potential secret detected")
            break


def main():
    if not LESSONS_DIR.exists():
        print(f"WARN  {LESSONS_DIR.relative_to(ROOT)} does not exist, nothing to validate")
        return 0

    errors = []
    warnings = []
    seen_ids = set()

    files = sorted(LESSONS_DIR.rglob("*.md"))
    if not files:
        print(f"WARN  {LESSONS_DIR.relative_to(ROOT)} has no lesson files")
        return 0

    for file in files:
        validate_file(file, seen_ids, errors, warnings)

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    print(f"Checked {len(files)} lesson file(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
