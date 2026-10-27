# GPT-6 Agent 工程 Skills

[English](README.md) · [架构图](ARCHITECTURE.svg) · [GPT-6 Astra 官方文章](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) · [HERO](https://github.com/wanshuiyin/HERO-Anti-OverDefense)

针对 Agent 工程中的四类**真实问题**提供可复用、按需触发的 Skills。它们只是工作方法，不要求引入新的 Agent 平台。

| Skill | 触发条件 |
|---|---|
| [`agent-tool-reliability`](skills/agent-tool-reliability/SKILL.md) | 真实 API/MCP/CLI 工具接口出现参数错误、超时、异常返回，或需要实现调用边界 |
| [`agent-context-continuity`](skills/agent-context-continuity/SKILL.md) | 多轮/恢复任务丢失关键约束、状态或原始证据 |
| [`agent-workflow-recovery`](skills/agent-workflow-recovery/SKILL.md) | 工作流确实有分支、暂停恢复、副作用或重复失败 |
| [`agent-badcase-evidence`](skills/agent-badcase-evidence/SKILL.md) | 需要对照基线判断算法/代码修改的救回、破坏和泛化证据 |

## GPT-6 适配方式

按照 OpenAI 2026-09-11 的 GPT-6 Astra 建议，缩短 Skill 描述，按需读取参考资料，不强迫每个任务执行冗长清单。明确安全本地任务的**完成边界**：实现 → 跑受影响测试 → 修复 → 更新 README → 交付，不因首次实现可运行就提前停止。

本包遵循这些设计原则，但尚未声称真实 GPT-6 Astra/Codex 行为测试已通过。用 [`MODEL_EVALUATION.md`](MODEL_EVALUATION.md) 的实际场景在目标模型里验证即可，不需要制造复杂测试平台。

HERO 使用 [作者维护的官方契约](https://github.com/wanshuiyin/HERO-Anti-OverDefense/blob/main/RULES.md)，不把整份案例库或重复规则复制进所有 Skills；这也避免规则不同步。真实可达的故障、必要验证以及项目已有审批范围始终有效。

## 安装和使用

仅复制需要的 Skill 目录：Codex 使用项目 `.agents/skills/` 或个人 `~/.agents/skills/`，Claude Code 使用 `.claude/skills/` 或 `~/.claude/skills/`。选读 [`AGENTS_SNIPPET.md`](AGENTS_SNIPPET.md) 的简短示例，不把四份 Skill 全部粘贴进通用指令。

技术栈沿用 Python/PyTorch、已有 Codex、MCP/CLI、JSON/JSONL 与当前 HTTP 客户端。只有存在相应实际需求时才选 Pydantic、SQLite、向量检索或 LangGraph。详细决策见 [`TECH_STACK.md`](TECH_STACK.md)。

可选只读工具演示提供四项离线测试：

```bash
python -m unittest discover -s tests -v
```

公开包不包含私有实验数据与本地路径。遵循“短文件、职责分离、函数简短中文注释、每次代码修改同步 README”的工程规范。开源协议：MIT。
