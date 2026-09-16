# Reference: Phases 3, 4, 4b, 4c, 6 — Capture, Test, Eval, Prune, Review

Load this file at the end of a build, or when writing tests, capturing learnings, running the functional eval, or preparing a build summary.

---

## Phase 3 — Capture Learnings

**During and after development**, capture what was learned.

**When something fails:**
- Do not silently fix it.
- Immediately add a `## Troubleshooting` or `## Known Issues` section to SKILL.md.
- Document: what failed, why it failed, what the fix was, and any constraints or gotchas.

**When something works but was non-obvious:**
- Write it into the skill as a note, comment, or reference entry.
- Future Claude instances have no memory of this session. The skill is the only place knowledge persists.

**Format for Troubleshooting entries:**

```markdown
## Troubleshooting

### [Short description of the issue]
**Symptom**: What happens / what error appears
**Root cause**: Why it happens
**Fix**: What resolves it
**Gotchas**: Anything to watch out for when applying the fix
```

---

## Phase 4 — Test As You Go

Write tests **alongside each feature**, not after the skill is complete.

Rules:
- Every major behavior gets at least one test case or eval prompt before moving to the next feature.
- Any time functionality is added, changed, or fixed: add or update the corresponding test.
- Treat regression prevention as part of implementation, not a separate step.

**Where to store tests:**
- Place test cases in `tests/evals.json` within the skill directory.
- Follow the schema from `skill-creator/references/schemas.md`.
- Each test entry should include: the trigger prompt, expected behavior, and at least one assertion.

**Minimum test coverage per skill:**
- At least 3 trigger prompts that *should* invoke the skill
- At least 2 prompts that *should not* invoke the skill (negative cases)
- At least 1 test per major workflow step or output type

If the user says "skip tests for now," acknowledge it and add a `## Tests Needed` section to SKILL.md listing what should be covered before the skill is considered production-ready.

---

## Phase 4b — Functional Eval (Fresh Session, 3 Subagents)

`tests/evals.json` checks whether the skill **triggers**. This checks whether it **works**. Run it before calling any skill done, and again after any edit that changes behavior.

Ask the user for a real test input if one isn't obvious: "What's a real input I should run this against?"

Spawn **3 subagents in parallel**, each running the skill against that input in a fresh context (nothing from the build session carries over). Each returns pass/fail plus the evidence for:

1. **Order** — did it execute the steps in the order SKILL.md lays out?
2. **Reference loading** — did it load the reference file each step names, *at that step*, and not all of them upfront?
3. **Connector** — did it call the connector or MCP correctly and return only the clean result? (Skip if the skill has none.)

**Pass requires all three.** Any failure is the next fix: adjust the skill, re-run. This loop is part of building, not an optional extra.

When a run doesn't do what SKILL.md says, **ask the agent why first.** It can usually name the ambiguous instruction or the wrong line in its own reference file. Fix that, then re-run.

For skills where "correct" is subjective (copy, analysis, judgment), also write 2–3 concrete criteria for a good output and check the runs against them. Keep them simple and specific.

**Report format:** what passed, what failed, and the specific fix for each failure.

---

## Phase 4c — Prune

Before shipping, run the deletion test over SKILL.md and every reference file. Full procedure and checklist: `references/prune.md`. Report line count before → after.

---

## Phase 6 — Build Review Summary

When the skill is complete (or a meaningful milestone is reached), deliver:

```
## Build Summary

### What was built or changed
[bullet list of what's new or different]

### Brainstorm ideas used
[which Phase 1 ideas made it into the implementation, and which were deliberately deferred]

### Tests and evals added or updated
[list of test files touched and what they cover]

### Functional eval result
[Phase 4b: order / reference loading / connector — pass or fail with the fix applied]

### Prune result
[Phase 4c: what was cut, line count before → after]

### Lessons learned written back
[any Troubleshooting or Known Issues entries that were added, and why]

### Version
[confirm the current version number and that the changelog was updated]
```

Then ask:

> "Should we do an optimization pass to make this skill faster and more efficient? I'll only suggest changes that don't break functionality, and I'll explain the tradeoffs before making any."

Subagents are fine in an optimization pass where `references/connectors.md` allows them (connector calls, research, evals) — not for the skill's core process.

Wait for the user's answer before optimizing.

---

## Default Priorities

When making tradeoff decisions during a build, use this order:

1. **Reliability** — it must work correctly every time
2. **Maintainability** — future Claude instances must be able to understand and update it
3. **Clarity** — instructions must be unambiguous
4. **Test coverage** — behavior must be verifiable
5. **Efficiency** — fast is good, but only after the above are satisfied

---

## Environment Notes

### Claude Cowork
- No browser/display. When generating eval viewers, use `--static <output_path>` and give the user a link to the HTML file.
- After running tests, always generate the eval viewer via `generate_review.py` before evaluating results yourself.

### Claude Code
- Eval viewer can open in browser directly.
- Description optimization via `run_loop.py` is available and should be run after Phase 6.
