---
name: agent-tool-reliability
description: Diagnose or implement an actual LLM-to-API, MCP, or CLI tool boundary with schema, timeout, or retry failures. Use only when that boundary is involved.
---

# Tool reliability

Inspect the **actual caller** and its existing SDK retry/timeout behavior. Define or reuse only the input/output fields consumed downstream. Validate inputs before invocation and relevant results before subsequent steps.

Classify the observed failure: a schema mismatch needs a precise correction; 401/403 needs configuration or authorization; a legitimate empty response remains empty; transient 429/502/503/504 may justify bounded backoff within a total budget. Honor `Retry-After` when present. Do not retry a deterministic invalid result.

For a write that times out, completion is unknown. Query its result or use the service's existing idempotent operation before resubmitting. Do not add generic transaction, deduplication or fingerprint frameworks to a local read-only task.

Implement the smallest change at the real boundary. Test the reachable failure that motivated it and any downstream contract it could break. Report failure clearly if the source problem remains.

An optional read-only demonstration lives in the source package’s `examples/` directory; it is not required to use this skill and does not implement a network timeout.
