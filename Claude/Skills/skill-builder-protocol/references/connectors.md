# Reference: Connectors, MCP, and Subagents

Load this file when the skill being built or edited touches a connector, an MCP tool, live research, or a web fetch — and whenever deciding whether a step should run in a subagent.

---

## 1. Adding a Connector Is a Decision, Not a Default

A connector floods context with tool schemas and verbose responses. After a large tool result, the agent frequently loses the skill's own process and starts improvising.

Decide in this order and **stop at the first that fits**:

1. **Do you need live data at all?** If the data is fairly stable — ICP, brand voice, product list, pricing, templates, style rules, folder paths — put it in a reference file and use **no connector**. Check this first, every time.
2. **If you need live data, put the call behind a subagent.** The subagent does the heavy interaction and returns a small, clean result. The main context keeps the skill's process intact.
3. **If a subagent isn't possible,** make the skill's scope extremely tight: one small action with the tool and nothing else.

**Ranking:** no connector > connector behind a subagent > connector inside a broad skill. Avoid the last.

If a connector or research step is heavy enough to dominate the skill, **split it into its own skill** and chain the two.

---

## 2. Subagent Policy

This supersedes any older blanket "no subagents" instruction. Subagents are allowed for work that returns a small result and keeps the main context clean — and only for that.

| Use a subagent for | Never use a subagent for |
|---|---|
| Connector / MCP calls with verbose payloads | The build itself — writing SKILL.md and reference files |
| Live research, scraping, web fetches | The interview, the brainstorm, or any human-in-the-loop step |
| The Phase 4b functional eval (`references/phases.md`) | Anything where the main thread needs the reasoning, not just the answer |
| Bulk mechanical reading across many files | Decisions the user has to approve |

Rules:

- The subagent returns the **clean result**, never the raw dump.
- The SKILL.md step must state what the subagent is expected to return.
- Pick the cheapest model that fits the subagent's job.

---

## 3. Checklist

- [ ] Every connector in the skill survived step 1 — it genuinely needs live data
- [ ] Static data moved to a reference file instead of being fetched at runtime
- [ ] Live calls sit behind a subagent, with the expected return shape stated in the step
- [ ] Heavy connector or research steps split into their own skill if they dominate
- [ ] No subagent used for the build, the interview, the brainstorm, or an approval step
