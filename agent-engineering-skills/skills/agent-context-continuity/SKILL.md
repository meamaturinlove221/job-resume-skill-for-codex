---
name: agent-context-continuity
description: Recover a material constraint, state, or evidence source lost during a multi-turn or resumed agent task. Use when forgetting or retrieval drift affects the result.
---

# Context continuity

Find the real source of the forgotten fact: current task constraints, task state, historical decisions, and original source files are different kinds of evidence. Prefer an existing state file, experiment record or code path over an old chat summary.

Trace the failure once: **not persisted → not retrieved → retrieved but trimmed → included but ignored**. Fix the stage actually responsible. Preserve links to the original source and its applicable version, not a second natural-language truth database.

For retrieval, first search exact task IDs, filenames, function names and protocol keys. Use broad semantic RAG only when a real corpus and observed search miss warrant it. Compress repeat logs and irrelevant context, but keep the decision-changing constraints.

Give the agent just enough current facts to resume the requested work. No compulsory per-turn full-history reload, vector database or periodic memory audit.
