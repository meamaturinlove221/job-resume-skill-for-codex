# GPT-6 Agent Engineering Skills

[中文说明](README_CN.md) · [Architecture](ARCHITECTURE.svg) · [OpenAI GPT-6 Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) · [HERO](https://github.com/wanshuiyin/HERO-Anti-OverDefense)

Four **opt-in**, narrowly triggered skills for coding agents working with real tool failures, context loss, resumable workflows, and scientific/regression evidence. They extend an existing project workflow; they are not an agent framework or a replacement for one.

| Skill | Load only when… |
|---|---|
| [`agent-tool-reliability`](skills/agent-tool-reliability/SKILL.md) | An LLM-facing API/MCP/CLI tool boundary is being implemented or is failing. |
| [`agent-context-continuity`](skills/agent-context-continuity/SKILL.md) | A resumed or multi-turn task loses a material constraint, state, or evidence source. |
| [`agent-workflow-recovery`](skills/agent-workflow-recovery/SKILL.md) | Real branching, interrupted execution, side effects, or repeated failures need recovery logic. |
| [`agent-badcase-evidence`](skills/agent-badcase-evidence/SKILL.md) | A model, experiment, or code fix must be judged against paired baseline cases and regressions. |

## GPT-6 / Astra fit

OpenAI's September 11, 2026 article recommends short, precise skill descriptions, progressive disclosure, less prescriptive step-by-step scaffolding, and a smaller task-relevant `AGENTS.md`. GPT-6 Astra may test thoroughly yet return too early at the first working implementation; completion boundaries should be explicit.

This pack follows those **documented prompt-design recommendations**. It is *not* claimed to be behaviorally validated on a live GPT-6 Astra/Codex run. See the [concrete evaluation prompts](MODEL_EVALUATION.md) for a small, manual check of activation and follow-through.

The [HERO contract](https://github.com/wanshuiyin/HERO-Anti-OverDefense/blob/main/RULES.md) is an independently maintained behavioral rule, **not duplicated here**. Install it in the host's always-loaded instructions when useful. A generic anti-over-defense rule must not suppress a real, reachable defect or a project-required test.

## Install (explicit opt-in)

**Codex** — copy only the relevant `skills/<skill-name>` directory into your repo's `.agents/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/`.

**Claude Code** — copy only the relevant directory into `.claude/skills/<skill-name>/` or `~/.claude/skills/<skill-name>/`.

Use [`AGENTS_SNIPPET.md`](AGENTS_SNIPPET.md) as optional *guidance*, not a mandatory global template. Skills must not be injected verbatim into every prompt. For an unrelated typo fix, none of these skills should load.

## Minimal technology stack

Use the infrastructure already implemented in the project:

| Concern | Default | Add something only when… |
|---|---|---|
| Research execution | Python/PyTorch and existing compute backend | Existing workflow cannot execute the required experiment |
| Tool contract | Existing validation, Pydantic if useful | Cross-boundary input/output needs typed validation |
| HTTP requests | Existing SDK or HTTPX | Explicit timeouts/retry responsibility is missing |
| State | Existing JSON/JSONL or run metadata | Concurrent writers need SQLite or another store |
| Context/retrieval | Source paths, reports, targeted search | The actual corpus justifies more retrieval machinery |
| Tool access | Existing CLI, SDK, or MCP tools | A needed action has no usable interface |
| Orchestration | Simple Python control flow | Checkpoints and nontrivial branch recovery justify a state graph such as LangGraph |
| Agent implementation | Existing Codex / Claude Code workflow | An independent unattended service is actually required |

See [technology decisions](TECH_STACK.md) for task-based selection. No default CrewAI, Redis, vector database, multi-agent reviewer, or new service is required.

## Optional example

`examples/read_only_tool.py` demonstrates one **read-only**, bounded retry policy. It does not implement an HTTP request timeout; real callers must configure that in the HTTP client. Four focused, fully offline tests exercise reachable input, temporary error, output, and retry-budget cases:

```bash
python -m unittest discover -s tests -v
```

No API credentials or GPU needed. For a different API, use its real error model rather than copying this example as a universal wrapper.

## Maintenance and limits

- Keep functions small, responsibilities separate, and Chinese comments on code functions; every code edit updates the relevant README.
- Existing VAF/VKF/evidence conventions remain authoritative **where they are used**. Do not require a full audit or new task directory for a one-line change.
- A passing runtime test is not a scientific improvement; use a matched control and report rescued and broken cases.
- Do not commit sensitive datasets, private machine paths, model checkpoints, accounts, or unpublished measurements into a public skills package.
- The skill files are reusable guidance, not installed production components. Use [evaluation prompts](MODEL_EVALUATION.md) to check model behavior in the real target host.

MIT licensed; see [`LICENSE`](LICENSE).
