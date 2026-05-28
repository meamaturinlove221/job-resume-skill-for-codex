# AGENTS.md — Job Resume Skill for Codex

This repository is a Codex-native adaptation of a Claude Code job-resume workflow.

## Goal

Make the repository usable as a Codex skill through:

```text
.agents/skills/job-resume-codex/SKILL.md
```

The original Claude Code slash-command files under `skills/` are retained only as historical references. Codex should prefer the `.agents/skills/job-resume-codex/` implementation.

## Repository architecture

```text
job-resume-skill-for-codex
├── README.md
├── AGENTS.md
├── .agents/skills/job-resume-codex/
│   ├── SKILL.md
│   ├── assets/
│   ├── references/
│   └── scripts/
├── skills/                 # legacy Claude Code command references
├── templates/              # legacy templates
└── examples/               # profile templates
```

## Truthfulness rules

Never fabricate resume facts. Do not invent internships, awards, papers, users, star counts, production metrics, or completed research results.

For VGGT/SMPL-X/4K4D claims, always distinguish:

- teacher vs student
- metric pass vs visual pass vs advisor pass
- diagnostic evidence vs final evidence

Do not present isolated scatter, projection overlay, teacher-only result, SMPL-only result, Kinect fusion, RBF prototype, or any proxy evidence as final advisor-level full-scene point cloud success.

## Default resume routing

- CV / 3D vision / graphics: VGGT-primary
- AI Agent / RAG / LLMOps / MCP / tooling: TuringResearch-primary
- Multimodal / AI engineering: balanced
- General engineering: C/C++/Python safe version

Do not add Java, Go, Rust, frontend frameworks, or Thermal-Gaussian/OMMG by default.

## Verification before committing changes

Before claiming the repository is Codex-ready, verify:

1. `.agents/skills/job-resume-codex/SKILL.md` exists.
2. `SKILL.md` has frontmatter with `name` and `description`.
3. README installation steps use `.agents/skills`, not `~/.claude/commands`.
4. README usage examples use `$job-resume-codex` or `/skills`, not Claude-only `/resume` or `/job-hunt` as primary commands.
5. Claim-safety rules are present.
