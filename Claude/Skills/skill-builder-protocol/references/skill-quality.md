# Reference: What Makes a Good SKILL.md (Artifact Quality)

Load this file while **writing or revising the content of a skill** — authoring the `description` (§1), deciding script vs inline (§2), splitting content into reference files (§3), setting the invocation mode (§4), adding human-in-the-loop checkpoints and options (§5), embedding the self-improvement rule (§6), or running the final quality gate (§7).

This file covers the *quality of the produced artifact*. It is the complement to the phase/process discipline in the other reference files: those govern *how you work*, this governs *what you ship*.

---

## 1. The Description Is the Trigger Surface

> ⛔ **SKIP THIS ENTIRE SECTION on the Claude Code path.** A Claude Code `SKILL.md` has **no YAML frontmatter and no description** (`references/claude-code-skill.md` RULE CC-0) — auto-triggering is deliberately disabled; `/<slug>` is the only entry point. §1 applies **only** to packaged / Cowork `.skill` builds. §7 (artifact quality gate) still applies to both.

The `description` in the YAML frontmatter is **the only thing the agent sees when deciding whether to load this skill.** It is surfaced in the system prompt alongside every other installed skill's description. The agent reads them all and picks based on the user's request. A vague description means the skill silently never fires — or fires on the wrong requests.

**Goal:** give the agent exactly enough to know (a) what capability the skill provides, and (b) when/why to trigger it (keywords, contexts, file types).

**Format rules:**
- **Max 1024 characters.**
- **Third person.** Describe the skill, never address "you."
- **Sentence 1 = the capability** (what it does).
- **Sentence 2 = the triggers** — literally start it with `Use when …` and list concrete phrases, contexts, or file types.
- **Never include personal names** — use "the user."

**Good:**
```
Extract text and tables from PDF files, fill forms, and merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```
Leads with capability, then gives the agent concrete triggers (PDF files, the words "PDF / forms / extraction").

**Bad:**
```
Helps with documents.
```
Gives the agent no way to distinguish this from every other document skill — it will misfire or never fire.

**Keep it tight.** The description is a trigger surface, not a rulebook. Rules ("never skip X", "always do Y") belong in the SKILL.md body — the body loads once the skill fires, so a rule in the description is paid for on every request and read on almost none. Aim for two sentences, roughly 200–450 characters. This skill's own frontmatter is the worked example.

---

## 2. When to Add a Script vs. Inline Instructions

Default to **inline instructions**. Add a script in `scripts/` only when at least one is true:

- **The operation is deterministic** — validation, formatting, parsing, a fixed transform. The same logic should run the same way every time.
- **The same code would otherwise be generated repeatedly** — every run re-writing the same snippet wastes tokens and invites drift.
- **Errors need explicit handling** — a real failure mode the instructions can't reliably catch by prose alone.

A script **saves tokens and improves reliability** versus code the agent regenerates from scratch each run. If none of the three holds, prose instructions are simpler to maintain — don't add a script just to have one.

---

## 3. Progressive Disclosure — Keep SKILL.md Lean, References One Level Deep

The SKILL.md body is loaded into context on every trigger. Detail that isn't needed every time belongs in a reference file that's loaded on demand (this skill's own routing table is the model).

**SKILL.md length:** aim for a lean body (~100–200 lines). **500 lines is a hard ceiling** — past that, split. Push detail into `references/`.

**Split content into a reference file when:**
- SKILL.md is drifting past ~150–200 lines.
- The content covers distinct domains (e.g. finance schemas vs. sales schemas) that are rarely needed together.
- A section is advanced or rarely-needed — most sessions won't touch it.

**References one level deep.** A reference file may be loaded from SKILL.md. It should **not** route to yet another file that routes to another. One hop from the router. Deeper nesting means the agent can't predict what it's loading and quietly misses content.

Verify it, don't eyeball it — run `grep -rn '](.*\.md)' references/` from the skill folder. Every hit is a reference file pointing at another file, i.e. a second hop. A handful of cross-links is a note; dozens means the reference layer has become its own web and the router no longer predicts what a step loads.

---

## 4. Invocation Mode — Human-Triggered by Default

Every AI-invocable skill's description sits in context on **every request**, used or not, and it can auto-fire when the user didn't want it.

**Default for a new skill: turn auto-invocation off.**

```yaml
disable-model-invocation: true
```

The skill then runs only when the user types `/<slug>`. Keep the description — it is the display fallback in the skill list, and it does not re-enable auto-firing (`disable-model-invocation: true` wins).

**Turn auto-invocation ON only when hands-free triggering is worth that standing cost:**

- The skill must fire in sessions where the user wouldn't think to invoke it (guardrails, protocols, safety checks).
- A scheduled task or routine runs it unattended.
- Missing the trigger is worse than firing when it wasn't needed.
- Its value is grounding answers in the user's own private data, so answering without it is worse than a misfire.

Ask the user which they want at build time, with a recommendation. On an edit, test the existing skill's mode against the same four questions as part of the upgrade pass — **and give a hard pass or fail, not a soft one.** A yes to any question is a pass with the reason named; no yes is a fail, and the fix is to add `disable-model-invocation: true`.

> `skill-builder-protocol` itself is a deliberate exception: it stays AI-invocable because its whole job is catching skill work in sessions where the user didn't type the command.

---

## 5. Human-in-the-Loop — Checkpoints and 3–5 Options

**Checkpoints.** The built skill must stop and ask before any consequential action: send, publish, post, spend, delete, overwrite, or any live external write. Source these from the judgment calls surfaced during the interview.

**3–5 options at every design choice.** Wherever the built skill asks the user to make a design or creative decision — format, tone, structure, headline, naming, which data source, output shape — it must present **3–5 concrete, distinct, numbered options and wait**. Never advance on a single suggestion. Never make the user ask for alternatives.

Write this into the step itself, not as a general aspiration:

> Present 3–5 distinct subject-line options, numbered, with your recommendation as option 1 and one line on why. Wait for the user to pick before drafting the body.

Rules for the options:

- **Genuinely distinct** — not one idea reworded four ways.
- **Recommendation is option 1**, with one line of reasoning.
- **Concrete** — show the actual option, not a description of it.
- **Exception:** for factual questions only the user can answer (a real folder path, a real deadline), a single question with a recommendation is correct. Options are for design choices.

---

## 6. Embed Self-Improvement and Save Good Outputs

Every skill ships with a rule that lets it improve as it runs. Paste this into the built skill's SKILL.md and point it at that skill's real files:

```markdown
## Self-improvement

- When the user corrects how a step was done, ask whether that correction should become a permanent part of this skill. If yes, update the step or reference file it belongs to. Never update the skill silently.
- When a correction is a hard rule, add it here phrased as do-this / don't-do-that, specific enough to catch every variant.
- When the user says an output was genuinely good, ask whether to save it to `references/examples/` as a model for future runs.
- Any change made this way gets a version bump and a CHANGELOG row.
- After adding anything, run the deletion test and cut what no longer changes behavior.
```

Adapt the paths to the skill's real reference files. Create `references/examples/` the first time an output is saved. Keep it short — it's guidance, not a manual.

**Always ask the confirmation question first.** A silent skill edit is how a one-off preference becomes a permanent rule nobody agreed to.

---

## 7. Finished-Artifact Quality Gate

Before packaging the `.skill` (or, on the Claude Code path, before telling the user it's ready), verify the *output*. This is distinct from the process Sync Checklist in `edit-skill.md`, which verifies you followed the workflow.

- [ ] **Description** leads with capability and has an explicit `Use when [triggers]` clause (third person, ≤1024 chars, no personal names, two sentences).
- [ ] **Invocation mode set deliberately** — `disable-model-invocation: true` unless the skill met a §4 exception.
- [ ] **SKILL.md is lean** (~100–200 lines; ≤500 hard ceiling) with detail pushed to `references/`.
- [ ] **Steps are instructions** — each step says what to do, with no preamble or rationale.
- [ ] **Progressive disclosure** — every step names the one reference file it needs; references one level deep, none routing to another.
- [ ] **Connectors pass `references/connectors.md`** — static data in a reference file, live calls behind a subagent.
- [ ] **Human checkpoints** before consequential actions, and 3–5 options at every design choice.
- [ ] **Self-improvement rule embedded** and pointing at this skill's real files.
- [ ] **No time-sensitive info** baked into instructions (no "as of this week," no soon-stale dates in the body).
- [ ] **Consistent terminology** — the same thing is called the same name throughout.
- [ ] **Concrete examples present** — at least one real input→output or good-vs-bad example, not only abstract rules.
- [ ] **Scripts justified** — every script in `scripts/` meets at least one test in §2.
- [ ] **Prune pass run** (`references/prune.md`) and the functional eval passed (`references/phases.md` Phase 4b).

If any item fails, fix it and re-run the gate.
