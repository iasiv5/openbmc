#!/usr/bin/env python3
import datetime as dt
from pathlib import Path
import sys


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".github").exists() and (candidate / "README.md").exists():
            return candidate
    return start.parents[2]


ROOT = find_repo_root(Path(__file__).resolve())
LESSONS_DIR = ROOT / "docs" / "lessons" / "entries"
INDEX_FILE = ROOT / "docs" / "lessons" / "index.yaml"


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    block = text[4:end]
    return parse_simple_yaml(block)


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
            data[key] = [v.strip().strip('"\'') for v in inner.split(",") if v.strip()] if inner else []
        else:
            data[key] = value.strip('"\'')
        i += 1
    return data


def quoted(v):
    text = str(v)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def write_yaml(entries):
    lines = []
    lines.append("version: 1")
    lines.append(f"updated_at: {dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}")
    lines.append("entries:")
    for e in entries:
        lines.append(f"  - id: {quoted(e.get('id', ''))}")
        lines.append(f"    title: {quoted(e.get('title', ''))}")
        lines.append(f"    date: {quoted(e.get('date', ''))}")
        lines.append(f"    component: {quoted(e.get('component', ''))}")
        lines.append(f"    topic: {quoted(e.get('topic', ''))}")
        lines.append(f"    failure_mode: {quoted(e.get('failure_mode', ''))}")
        lines.append(f"    impact: {quoted(e.get('impact', ''))}")
        lines.append(f"    confidence: {quoted(e.get('confidence', ''))}")
        lines.append(f"    sensitivity: {quoted(e.get('sensitivity', ''))}")
        lines.append(f"    status: {quoted(e.get('status', ''))}")
        lines.append(f"    owner: {quoted(e.get('owner', ''))}")
        lines.append("    tags:")
        for t in e.get("tags", []):
            lines.append(f"      - {quoted(t)}")
        lines.append(f"    path: {quoted(e.get('path', ''))}")
    lines.append("")
    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    entries = []
    if LESSONS_DIR.exists():
        for path in sorted(LESSONS_DIR.rglob("*.md")):
            data = parse_frontmatter(path.read_text(encoding="utf-8"))
            if not data:
                continue
            entries.append(
                {
                    "id": data.get("id", ""),
                    "title": data.get("title", ""),
                    "date": data.get("date", ""),
                    "component": data.get("component", ""),
                    "topic": data.get("topic", ""),
                    "failure_mode": data.get("failure_mode", ""),
                    "impact": data.get("impact", ""),
                    "confidence": data.get("confidence", ""),
                    "sensitivity": data.get("sensitivity", ""),
                    "status": data.get("status", ""),
                    "owner": data.get("owner", ""),
                    "tags": data.get("tags", []) if isinstance(data.get("tags"), list) else [],
                    "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                }
            )

    entries.sort(key=lambda e: (e.get("date", ""), e.get("id", "")), reverse=True)
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(entries)
    print(f"Wrote {INDEX_FILE.relative_to(ROOT)} with {len(entries)} entr{'y' if len(entries)==1 else 'ies'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
