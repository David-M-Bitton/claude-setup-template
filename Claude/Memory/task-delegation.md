# Task Delegation

Spawn subagents to isolate context, parallelize independent work, or offload bulk mechanical tasks. Use them liberally when they keep the main context clean. Don't spawn when the parent needs the reasoning, when synthesis requires holding things together, or when spawn overhead dominates.

Pick the cheapest model that can do the subtask well:
- **Haiku** — bulk mechanical work, no judgment.
- **Sonnet** — scoped research, code exploration, in-scope synthesis.
- **Opus** — subtasks needing real planning or tradeoffs.

Rules:
- One task per subagent for focused execution.
- Maximum spawn depth is 2 (parent → subagent → one further tier).
- Haiku does not spawn further subagents. If it needs to, the task was wrong-sized — return to the parent.
- Don't escalate tiers without a concrete reason. If a subagent realizes it needs a higher tier, return to the parent instead of spawning up.
- Parent owns final output and cross-spawn synthesis.
- User instructions override.
