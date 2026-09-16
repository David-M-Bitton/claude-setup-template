# {Skill Name} — Project Instructions

This folder is the working directory for the **{Skill Name}** skill and its {skill purpose} work. It holds the skill, the per-task work files, and the change logs. Copy this `0-template/` folder as the starting point for any new skill project.

---

## Folder map

```
{skill-name}/                           ← project root (this folder)
├── CLAUDE.md                           ← you are here (read this every session)
├── skill/                              ← THE skill. All edits go here.
│   ├── SKILL.md
│   ├── CLAUDE.md                       ← skill-internal rules (don't confuse with this file)
│   ├── CHANGELOG.md                    ← update on every skill change
│   ├── references/                     ← use as needed
│   ├── scripts/                        ← use as needed
│   └── tests/
│       └── evals.json                  ← add a test when you fix a recurring mistake
├── outputs/                            ← per-task work files (one md per run)
│   └── YYYY-MM-DD - {Task-Name}.md     e.g. "2026-05-07 - CRM.md"
├── random/                             ← scratch / drafts / notes (no rules here)
├── MEMORY.md                           ← skill-specific facts (read every session)
```

**Never create files or folders directly in this project root.** Route everything:
- New work → `outputs/YYYY-MM-DD - {Task-Name}.md` (use today's date)
- Skill edits → inside `skill/`
- Scratch / experiments → inside `random/`

---

## Memory System

At session start, read `./MEMORY.md` before responding. Use what you find to inform your work. Don't announce what you found, just be informed by it.

When the user says "remember this," write the information to `MEMORY.md` immediately and confirm. If you think something should go into `CLAUDE.md` or `MEMORY.md`, tell the user.

**Where things go:** Apply two tests when deciding where to save something.
- **Test 1 — Does it prescribe behavior?** Look for words like "always," "never," "before doing X, do Y." If yes, add it to this `CLAUDE.md` under the appropriate section.
- **Test 2 — Does it describe a fact about the world that could change?** Contact details, project status, decisions, things the user told you to remember. If yes, add it to `MEMORY.md`.

When unsure, suggest which file you think it belongs in and ask the user to confirm.

---

## Core rules

### 1. The skill lives in the inner `skill/` folder
When the user says "run the skill" or "update the skill," that's where you work — the `/skill/` subfolder that contains `SKILL.md`, `CHANGELOG.md`, and optionally `references/`, `scripts/`, or `tests/`. Don't write skill files at the project root.

### 2. New work → `outputs/` folder
When the user asks for a new run of the skill (analysis, research, draft, audit — whatever this skill does), write the output into:
`outputs/YYYY-MM-DD - {Task-Name}.md`
Example: `outputs/2026-05-07 - CRM.md`. Use today's date. Don't dump work into the project root or into `random/`.

### 3. Random / scratch → `random/` folder
Drafts, half-formed ideas, comparison notes, anything not ready to be a real output — put it in `random/`. No naming rules. This is the freeform space.

---

## Output workflow

1. **Read the skill first.** Open `skill/SKILL.md` and any relevant `references/` files before drafting anything. Lessons from past runs live there.
2. **Create the output file.** `outputs/YYYY-MM-DD - {Task-Name}.md` — use today's date.
3. **Do the work.** Follow the skill's process exactly. If the skill has a checklist, work through it in order.
4. **Show the draft, get approval, then act.** For anything that writes to an outside system (an account, a live site, a send), never push until the user explicitly approves.
5. **Verify after acting.** See "Verification Before Done" below.

---

## Tracking skill changes (CHANGELOG.md)

Every skill edit = version bump in `SKILL.md` + new row in `skill/CHANGELOG.md`. No silent changes. Use the `skill-builder-protocol` skill — it owns the full workflow.

**The full format rules live inside `skill/CHANGELOG.md` itself** (header preamble). Read them there — don't duplicate them here.

Bootstrap logic:
- **No `skill/` folder yet?** Do nothing. The skill doesn't exist.
- **`skill/` exists but no `CHANGELOG.md`?** Create it with the full preamble below, then add your first entry. **Then delete the `### Preamble to drop in...` subsection from THIS file** (the heading and the entire ` ```markdown ... ``` ` code block beneath it) so the rules live in only one place going forward.
- **`CHANGELOG.md` already exists?** Read the preamble at the top of that file and follow those rules. If you still see the `### Preamble to drop in...` subsection in this CLAUDE.md, **delete it from this file now** — it's a stale duplicate.

### Preamble to drop in when first creating `skill/CHANGELOG.md`

```markdown
# Changelog — {skill-name}

All notable changes to this skill are documented here.
Format: semantic versioning (MAJOR.MINOR.PATCH).
Date format: `YYYY-MM-DD at H:MM PM` — always run your system `date` command before writing a timestamp. Never guess.

Versioning:
- PATCH (`v1.0.0` → `v1.0.1`): typo, small wording tweak
- MINOR (`v1.0.0` → `v1.1.0`): new rule, new reference, meaningful addition
- MAJOR (`v1.0.0` → `v2.0.0`): restructure or breaking change

Rules:
- Every save of `SKILL.md` = version bump + new row here.
- Newest entry at the **top**, below this header block.
- Never delete old rows. Full history stays.
- Be specific. "Added rule against 'innovative' as a value-prop adjective" — not "Updated wording."
- `SKILL.md` must carry a version line directly after the YAML frontmatter:
  `**Version: v1.X.X** — Full history in [CHANGELOG.md](./CHANGELOG.md).`

Entry template (copy, fill, place at top):

## [v1.X.X] — YYYY-MM-DD at H:MM PM

### Added
- [What was added]

### Changed
- [What was changed]

### Fixed
- [What was fixed]

(Omit sections that don't apply.)

---
```

---

## Self-Improvement Loop

This is the most important section. Read it before responding to a correction.

- **After ANY correction from the user:** Confirm with the user that they want to update the skill with what you learned. Make the rule generic enough to apply across the skill's whole scope.
- **Write rules for yourself** that prevent the same mistake from happening again. Phrase them as do-this / don't-do-that, not as soft guidance.
- **Ruthlessly iterate** on these lessons until your mistake rate drops. If you make the same mistake twice, the rule wasn't strong enough — strengthen it.
- **Review lessons at session start** by reading `SKILL.md` and the relevant reference files before you start the work.
- **Add a new test to `tests/evals.json`** whenever you fix a recurring mistake, so the skill catches it next time.

---

## Verification Before Done

Never mark a task complete without proving it works.

- If you pushed something to an outside system, read it back and confirm the fields/status match what was approved.
- If you edited the skill, check `CHANGELOG.md` actually has the new row and `SKILL.md`'s version line bumped.
- If a step can't be done via the tool/API, say so out loud and tell the user exactly which manual step they need to do. Don't pretend it's done.

---

## Working style

- **Plain English.** If a sentence sounds like a consultant wrote it, rewrite it. An 18 year old should understand you. No jargon — if you have to use a technical term, say what it means in the same breath.
- **Show your work briefly.** When you make a non-obvious decision, say it in one line. Don't bury the user in reasoning.
- **One thing at a time.** Don't combine drafting, pushing to an API, and skill updates in a single uninterrupted run unless the user asked for that. Show the work, get approval, then push.

---

## Things to avoid

- ❌ Do not write files in any other directory on the computer. All work goes in this folder or its subfolders.
- ❌ Do not silently modify the skill. Every change needs approval, then skill version bump, then CHANGELOG entry.
- ❌ Marking a task done because the tool call returned 200. Verify the actual outcome.
- ❌ Restating the user's own words back at them in fancy language. Just answer. Less is more.
- ❌ Sharing secrets (API keys, webhook URLs, OAuth tokens) in chat or files. Env vars only.
