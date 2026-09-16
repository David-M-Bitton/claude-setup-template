# {Skill Name} — Project Instructions

Working directory for the {Skill Name} skill and its {skill purpose} work.

Global rules (response style, plain English, verification, self-improvement) live in `~/.claude/CLAUDE.md`. Memory tiers and folder conventions live in the parent `Skills/CLAUDE.md`. Only skill-specific rules go here.

---

## Folder map

```
{skill-name}/                          ← project root (this folder)
├── CLAUDE.md                          ← you are here (read every session)
├── MEMORY.md                          ← skill-specific facts (read every session)
├── skill/                             ← THE skill. All edits go here.
│   ├── SKILL.md
│   ├── CHANGELOG.md                   ← update on every skill change
│   ├── references/                    ← as needed (incl. config.json)
│   ├── scripts/                       ← as needed
│   └── tests/evals.json               ← add a test when you fix a recurring mistake
├── outputs/                           ← one file per run: "YYYY-MM-DD - {Task-Name}.md"
└── random/                            ← scratch / drafts (no rules here)
```

**Never write to this project root.** New work → `outputs/`. Skill edits → `skill/`. Scratch → `random/`.

---

## Output workflow

1. **Read `skill/SKILL.md`** and its relevant `references/` before drafting. Past lessons live there.
2. **Create** `outputs/YYYY-MM-DD - {Task-Name}.md` using today's date.
3. **Do the work** — follow the skill's process exactly, in order.
4. **Show the draft, get approval, then act.** If this skill does anything irreversible or external (publishing, sending, live writes), never execute before explicit approval.
5. **Verify:** read the result back, and confirm `skill/CHANGELOG.md` has the new row + `SKILL.md`'s version line bumped if you edited the skill.

---

## Skill changes

Every skill edit = version bump in `SKILL.md` + new row in `skill/CHANGELOG.md`. No silent changes. **Format rules live in `skill/CHANGELOG.md`'s own header** — read them there.

Bootstrap:
- **No `skill/` folder?** Do nothing — the skill doesn't exist.
- **No `CHANGELOG.md`?** Create it with the preamble below, add your first entry, then **delete the `### Preamble...` subsection from this file** (heading + code block) so the rules live in one place.
- **`CHANGELOG.md` exists?** Follow its preamble, and delete the `### Preamble...` subsection from this file if it's still here.

### Preamble to drop in when first creating `skill/CHANGELOG.md`

```markdown
# Changelog — {skill-name}

All notable changes to this skill are documented here.
Format: semantic versioning (MAJOR.MINOR.PATCH).
Date format: `YYYY-MM-DD at H:MM PM EST` — always run `TZ='America/New_York' date '+%Y-%m-%d at %I:%M %p'` before writing a timestamp. Never guess.

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

## [v1.X.X] — YYYY-MM-DD at H:MM PM EST

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

## Skill-specific rules

_{Add rules unique to this skill. Delete this line once you have some.}_

---

## Notes

- **Unattended runs** (scheduled task, or 10 PM–9 AM ET): auto-apply skill improvements (version bump + CHANGELOG entry as usual), then notify via the alert channel in `skill/references/config.json`. No channel configured? Leave a note at the top of the next `outputs/` file.
- **Constants** — account IDs, endpoints, paths, handles — go in `skill/references/config.json`. Read it before running so you don't ask for what's already saved.
- **One thing at a time.** Don't combine drafting, executing, and skill updates in one uninterrupted run unless asked.
- **Never put secrets** (API keys, webhook URLs, tokens) in chat or in files outside `config.json`/env vars.
