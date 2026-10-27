---
name: agent-badcase-evidence
description: Judge a model experiment or code fix against matched baseline cases, including rescued errors and regressions. Use when an improvement claim depends on evidence.
---

# Bad-case evidence

Restate the actual question and keep evaluation protocols comparable: same inputs, labels, split, baseline and scoring meaning. Use the project's existing logs and result files; do not build a second evidence platform.

For matched cases, record **rescued**, **broken**, still-correct and still-wrong results. Analyze the smallest relevant group: a high aggregate score may hide a missing registration class, a texture/background shortcut, or a changed label definition. Distinguish a completed evaluation, preserved performance and demonstrated improvement.

Trace material failure hypotheses to actual cases. Choose the next experiment only if its possible outcomes change the research decision. Report a meaningful regression plainly; preserve original baseline behavior unless a justified tradeoff supports changing it.

Load [`references/vision-research.md`](references/vision-research.md) only for image classification, 3D reconstruction or rendering experiments. Do not use it for ordinary program regressions.
