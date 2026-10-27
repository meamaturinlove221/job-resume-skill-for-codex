# Technology decisions

Treat this as guidance for **selecting** tools, not a list of things to install.

## Start with the working path

- Existing Python, PyTorch and available GPU/compute backend execute research jobs. Cloud services such as Modal are retained only when already required by the actual experiment.
- Codex/Claude Code perform analysis and code edits using existing shell, repository and MCP tools. A tool does not need to become its own MCP server.
- Python's existing typed checks are sufficient at small local boundaries. Pydantic is useful for shared external contracts, not as mandatory wrapping of every function.
- HTTPX or the current client must own real network timeouts; retries apply only to transient failures. Check whether SDK already retries. A write that timed out may still have taken effect.
- Existing JSON/JSONL, experiment output directories and source links usually suffice for task state. A database earns its place when concurrent writes, queries or transaction semantics are truly required.
- Retrieval starts from real code paths, experiment IDs and saved reports. Use RAG, embeddings or vector storage when concrete retrieval misses demonstrate value, not because a job title lists RAG.
- A linear program is a good workflow. Consider LangGraph only for real shared state, conditional transitions, long interruptions or human-in-the-loop resume.

## Completion, budgets and approvals

A safe local task should reach its defined outcome, then run the smallest meaningful verification. Specify completion before implementation instead of repeatedly pausing for permission on disposable fixtures. Respect stated training, real-data, deployment and externally visible write approvals.

For repeated failures, ask whether the failure condition changed. If not, stopping is better than paying for another identical call. Use the smallest state record that allows a real resume.

## Independent unattended Agent

Only after an actual unattended workflow exists should engineering expand to durable checkpointing, event logs, resource budgets and potentially a graph runtime. Monitor scientifically relevant outputs (dataset split, protocol, paired results) separately from operational success (a process finished).
