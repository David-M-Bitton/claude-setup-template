# Reference: Prune Pass (Phase 4c)

Load this file **before shipping any skill — new or edited.** Applies to SKILL.md and every reference file.

Every word in a SKILL.md costs tokens on every single run. Pruning is not tidying; it is the main lever on how well the skill performs.

---

## 1. The Deletion Test (primary tool)

For every paragraph, sentence, and rule: **if deleting it would not change what the agent does, delete it.**

Text that fails the test:

- **Instructions the agent already follows by default.** "Write a clear description" — it would do that anyway. No-op.
- **Encouragement with nothing concrete attached.** "Be thorough", "do a great job", "take your time".
- **Restated baseline good practice.** "Double-check your work before finishing."
- **Rationale living inside a step.** Explaining *why* belongs in a reference file, or nowhere.
- **Preamble.** "Before we begin, it's worth noting that…"

---

## 2. Steps Say What To Do — Nothing Else

In SKILL.md, every step is a plain instruction. If a line does not tell the agent what to do, cut it or move it to a reference file. Background, reasoning, examples, and long tables all live in `references/`, reached by a pointer from the step that needs them.

---

## 3. One Home Per Rule (single source of truth)

Every rule, table, template, and procedure lives in **exactly one file**. If it appears in two, the copies will drift and disagree, and a future session will follow the stale one.

- Keep it in the most specific file that needs it.
- Everywhere else, replace it with a one-line pointer naming that file.
- This applies across reference files, not just SKILL.md.

---

## 4. Clear Sediment

Accumulated half-relevant material:

- **Used by only one branch** → move it into that branch's reference file.
- **Stale or wrong** → delete it.
- **Irrelevant** → delete it.

---

## 5. Strip Bloat

No hedging, no throat-clearing, no time-sensitive phrasing ("as of this week", "recently"). One consistent term per concept — don't call the same thing three different names across three files.

---

## 6. Prune Checklist

- [ ] Deletion test run on every paragraph of SKILL.md and each reference file
- [ ] No no-ops left
- [ ] Every rule, table, and procedure has exactly one home; duplicates replaced with pointers
- [ ] Sediment cleared — branch-only material moved out, stale material deleted
- [ ] SKILL.md within ~100–200 lines (500 is the hard ceiling) — see `references/skill-quality.md` §3
- [ ] Language plain and direct, one term per concept

**Report the result:** what was cut, and line count before → after.

**Never delete content the user explicitly asked to keep.** If it fails the deletion test, say so and ask — don't remove it unilaterally.
