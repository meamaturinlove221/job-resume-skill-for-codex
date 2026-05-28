# Job Resume Skill for Codex

A Codex-native job-search and resume-tailoring skill converted from a Claude Code workflow.

It helps with:

- JD analysis and job-route classification
- targeted resume bullets
- Boss/牛客/实习僧 outreach messages
- interview drill questions
- risky-claim audits
- job-table screening

This fork is designed for Codex. The old Claude Code slash-command files are kept as references only.

## Why this fork exists

The upstream workflow used Claude Code slash commands such as `/resume` and `/job-hunt`, and installed files under `legacy Claude commands path`. Codex skills use a different structure: a skill directory with a `SKILL.md` file. This repository now provides that Codex-native structure.

## Architecture

```text
Input
  ├─ JD text
  ├─ job link content
  └─ CSV/XLSX job table
        │
        ▼
Codex skill: job-resume-codex
        │
        ├─ JD parser
        ├─ route classifier
        │     ├─ CV / 3D vision / graphics        → VGGT-primary
        │     ├─ AI Agent / RAG / LLMOps / tools   → TuringResearch-primary
        │     ├─ multimodal / AI engineering       → balanced
        │     └─ general C++ / Python engineering  → general-safe
        ├─ claim safety gate
        └─ output generator
              ├─ resume bullets
              ├─ outreach message
              ├─ interview drill
              └─ risk list
```

## Repository layout

```text
job-resume-skill-for-codex/
├── README.md
├── AGENTS.md
├── .agents/
│   └── skills/
│       └── job-resume-codex/
│           ├── SKILL.md
│           ├── assets/
│           │   ├── user_profile.md
│           │   ├── job_templates.json
│           │   └── resume_template.html
│           ├── references/
│           │   ├── resume_workflow.md
│           │   ├── job_hunt_workflow.md
│           │   └── claim_safety.md
│           └── scripts/
│               └── render_resume.py
├── skills/       # legacy Claude Code references
├── templates/    # legacy templates
└── examples/     # legacy profile templates
```

## Install for Codex

### Option A: repo-local skill

Use this when you open this repository in Codex. Codex can discover the skill from:

```text
.agents/skills/job-resume-codex/SKILL.md
```

Then call it in Codex with:

```text
$job-resume-codex
```

or use:

```text
/skills
```

and select `job-resume-codex`.

### Option B: global user skill

Copy the skill directory to your user skills folder:

```text
~/.agents/skills/job-resume-codex/
```

On Windows, the equivalent is usually:

```text
C:\Users\<YOUR_USER>\.agents\skills\job-resume-codex\
```

## Usage examples

### 1. Analyze one JD

```text
$job-resume-codex

下面是 JD。请输出：岗位路由结论、JD关键词分级、匹配矩阵、简历项目排序、可替换 bullets、自我介绍、面试拷打清单、风险表述清单。

JD:
...
```

### 2. Screen a job table

```text
$job-resume-codex

读取我给的岗位表。对每个岗位输出：方向路由、匹配等级、推荐简历版本、关键匹配点、风险点、自我介绍、面试准备重点。
```

### 3. Generate interview drills

```text
$job-resume-codex

这个岗位要投递。请按 CV/三维视觉路线，为 VGGT + SMPL-X、VGGT + ZJU-MoCap、VideoPose3D 准备面试拷打问题和安全回答边界。
```

## Route system

### CV / 3D vision / graphics route

Use for JDs mentioning computer vision, 3D vision, point cloud, depth estimation, camera geometry, human reconstruction, SMPL/SMPL-X, rendering, OpenCV, OpenGL, or graphics.

Project priority:

1. VGGT + SMPL-X / 4K4D human-prior full-scene point cloud work
2. VGGT + ZJU-MoCap data adapter
3. VideoPose3D
4. C++ graphics/game engineering
5. TuringResearch as research-engineering support

### AI Agent / RAG / LLMOps / tooling route

Use for JDs mentioning AI Agent, tool use, RAG, knowledge base, evaluation, LLMOps, MCP, workflow automation, AI coding, or research engineering.

Project priority:

1. TuringResearch / automated research workflow
2. evidence management, manifests, failure gates, source tracking
3. Codex / Claude Code / OpenCode workflow experience
4. VGGT as a complex research-engineering case
5. Python automation

### General engineering route

Use for broad C++ / Python engineering roles.

Project priority:

1. C / C++ / Python foundation
2. C++ graphics/game project
3. Python automation and data processing
4. Git / Linux / collaboration
5. Research projects as engineering complexity evidence

## Claim safety

This repository is intentionally conservative. It should improve wording, not invent facts.

Never fabricate:

- internships
- publications
- awards
- open-source stars or users
- production metrics
- completed model results
- ownership of work done by others

For VGGT-related projects, always distinguish:

- teacher vs student
- metric pass vs visual pass vs advisor pass
- diagnostic evidence vs final evidence

Do not present isolated human scatter, projection overlay, SMPL-only results, Kinect/teacher-only results, or prototype baselines as final advisor-level full-scene point cloud evidence.

## Optional HTML resume rendering

The skill includes a small helper:

```text
.agents/skills/job-resume-codex/scripts/render_resume.py
```

It renders a filled HTML file from `resume_template.html` and a JSON payload. PDF export requires local Chrome/Edge and should only be claimed if actually run in the local environment.

## Migration notes from Claude Code

| Claude Code version | Codex version |
|---|---|
| legacy Claude Code commands directory | `.agents/skills/job-resume-codex/SKILL.md` |
| `/resume` | `$job-resume-codex` with JD task |
| `/job-hunt search` | job-table workflow by default; browser automation optional |
| `/job-hunt apply` | job-table tailoring workflow |
| `~/.claude/.../user_profile.md` | `.agents/skills/job-resume-codex/assets/user_profile.md` |

## Status

Codex-ready skill structure is included. Browser job-board automation is not enabled by default because it depends on local login, browser tooling, and platform page behavior.
