---
name: agent-workflow-recovery
description: Repair a workflow with real branching, interrupted execution, repeated failures, or external side effects. Use when recovery semantics affect an actual task.
---

# Workflow recovery

Start from the current working execution path. A fixed sequence stays linear; only actual branching or long-running resumability calls for a state graph or LangGraph.

Reuse the existing task state and run artifacts. Keep the minimum resume data: task identity, last completed step, input/result references and permitted next action. A checkpoint remembers state; it does **not** roll back remote writes.

Retry only when the error is recoverable and some condition can change. Bound steps or retries at the scope that risks repeating. For side effects, check what actually happened before a retry; use native idempotency or an explicit compensating action when the service supports it.

Test the failure transition that originally motivated the change. If the task is local, safe and authorized, implement through the complete requested outcome; do not stop merely because the first branch runs.
