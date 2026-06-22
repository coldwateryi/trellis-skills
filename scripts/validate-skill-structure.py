#!/usr/bin/env python3
"""Validate Trellis skill package structure with no third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
FIELD_RE = re.compile(r"^(?P<key>[A-Za-z0-9_-]+):(?P<value>.*)$")
REFERENCE_RE = re.compile(r"`(references/[A-Za-z0-9._/-]+)`")


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")

    fields: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    for line in match.group("body").splitlines():
        field = FIELD_RE.match(line)
        if field and not line.startswith(" "):
            if current_key is not None:
                fields[current_key] = "\n".join(current_value).strip()
            current_key = field.group("key")
            current_value = [field.group("value").strip()]
            continue

        if current_key is not None:
            current_value.append(line)

    if current_key is not None:
        fields[current_key] = "\n".join(current_value).strip()

    return fields


def referenced_files(skill_md: Path) -> set[Path]:
    text = skill_md.read_text(encoding="utf-8")
    refs: set[Path] = set()
    for match in REFERENCE_RE.finditer(text):
        ref = match.group(1).rstrip(".,;:)，。；）")
        refs.add(skill_md.parent / ref)
    return refs


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    try:
        fields = parse_frontmatter(skill_md)
    except ValueError as exc:
        return [f"{skill_md}: {exc}"]

    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()

    if not name:
        errors.append(f"{skill_md}: missing name")
    elif name != skill_dir.name:
        errors.append(f"{skill_md}: name '{name}' does not match directory '{skill_dir.name}'")

    if not description:
        errors.append(f"{skill_md}: missing description")

    extra_fields = sorted(set(fields) - {"name", "description"})
    if extra_fields:
        errors.append(f"{skill_md}: unsupported frontmatter fields: {', '.join(extra_fields)}")

    if not (skill_dir / "agents" / "openai.yaml").is_file():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")

    for ref in sorted(referenced_files(skill_md)):
        if not ref.is_file():
            errors.append(f"{skill_md}: referenced file does not exist: {ref.relative_to(skill_dir)}")

    return errors


def main() -> int:
    root = Path.cwd()
    skill_dirs = sorted(path.parent for path in root.glob("*/SKILL.md"))
    if not skill_dirs:
        print("ERROR: no top-level skills found", file=sys.stderr)
        return 1

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: validated {len(skill_dirs)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
