#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
skill = root / ".agents" / "skills" / "job-resume-codex" / "SKILL.md"
readme = root / "README.md"
errors = []

if not skill.exists():
    errors.append("missing .agents/skills/job-resume-codex/SKILL.md")
else:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md missing YAML frontmatter")
    if "name: job-resume-codex" not in text:
        errors.append("SKILL.md missing name: job-resume-codex")
    if "description:" not in text:
        errors.append("SKILL.md missing description")

if not readme.exists():
    errors.append("missing README.md")
else:
    text = readme.read_text(encoding="utf-8")
    if "~/.claude/commands" in text:
        errors.append("README still uses Claude Code install path as primary path")
    if "$job-resume-codex" not in text:
        errors.append("README missing $job-resume-codex usage")

if errors:
    for e in errors:
        print(f"FAIL: {e}")
    sys.exit(1)
print("OK: Codex skill structure looks valid")
