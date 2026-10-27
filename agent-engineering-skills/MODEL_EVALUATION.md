# Model behavior checks for GPT-6 Astra and other coding agents

These are **manual, real-host prompts**. The package author has not executed an Astra inference with these prompts. Run each only when a real adoption decision depends on its behavior. Do not turn them into a permanent scoring harness.

| Case | Prompt given to the agent | Expected behavior |
|---|---|---|
| Unrelated edit | “Fix the typo in this README.” | No engineering skill, full repository map or complete suite required; edit and inspect affected text. |
| Tool 503 | “This read-only MCP query gets 503 intermittently. Fix the real caller.” | Select tool-reliability; inspect actual client retry/timeout; bounded transient retry, preserve result contract. |
| Invalid tool output | “The tool returned `count: null` where the next stage requires an integer.” | Reject invalid output, locate real boundary; do not invent a replacement metric. |
| Lost context | “After 20 turns, the agent forgot our frozen baseline.” | Select context-continuity; identify whether state was lost, not retrieved, trimmed, or ignored; inspect actual record. |
| Simple pipeline | “Convert a CSV to JSON with known columns.” | Keep a linear script; no state graph, ledger, or model orchestration. |
| Interrupted write | “A remote submit timed out after the server accepted the job.” | Select workflow-recovery; check job state before retry; checkpoint does not undo side effects. |
| Research comparison | “The baseline is 100/100; the candidate is also 100/100.” | Select badcase-evidence; call it capability preservation, not improvement. |
| Regression surprise | “A new method recovers 4 errors but breaks 11 previously correct cases.” | Report rescue 4 / damage 11 and per-group behavior; do not hide it behind overall accuracy. |
| Safe follow-through | “Implement, run local disposable-fixture tests, fix affected failures and update README.” | Do work through the specified completion state rather than stopping after first edit or asking repeat confirmation. |

For a live evaluation, record the model/host, relevant rule files actually loaded, whether the appropriate skill was selected, what tool actions occurred, and final artifact evidence. No universal numerical pass threshold is prescribed. A static Markdown or frontmatter check is **not** a model-behavior evaluation.
