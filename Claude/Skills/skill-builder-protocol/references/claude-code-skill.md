# Reference: Building a Claude Code Skill (not installed, easy to edit)

Load this file when the user chose **Claude Code skill** at the Step 0 gate in `new-skill.md` (the non-packaged option). If they chose **Cowork-installed skill**, ignore this file and follow the normal `new-skill.md` + `packaging.md` flow instead.

**Why this path exists:** A Claude Code skill is just a folder of plain files on disk. Nothing is zipped or installed. To change it later you edit the files directly — no repackaging, no re-import. That is the whole point of this option.

**This whole procedure is self-contained.** Everything needed to stamp out the folder lives inside THIS skill, in `assets/claude-code-template/`. Do **not** depend on the user having a `0-template` folder on their computer — most people won't.

---

## 🔴 RULE CC-0 — NEVER put YAML frontmatter in a Claude Code `SKILL.md`

**A Claude Code `SKILL.md` built on this path gets NO YAML frontmatter. No `---` block, no `name:`, no `description:`. The file starts with the version line.**

**Why:** frontmatter `description:` is the auto-trigger surface. Claude reads every installed skill's description at startup and fires the skill on its own judgement. That is not what this path is for. **A skill on this path fires only when the user types `/<slug>`** — explicit, never inferred. Frontmatter also costs tokens in the startup menu on every single session, used or not.

**DO** — first three lines of a Claude Code `SKILL.md`:

```markdown
# <Skill Name>

**Version: v1.0.0** — Full history in [CHANGELOG.md](./CHANGELOG.md).
```

**DON'T** — this is the packaged-skill format, wrong for this path:

```markdown
---
name: my-skill
description: Use when the user wants ...
---
```

**Scope of this rule:**
- ✅ Applies to **every** skill built on the Claude Code path (Step CC-5), and to any Claude Code skill you edit.
- ❌ Does **not** apply to the packaged **Cowork / `.skill`** path (`new-skill.md` + `packaging.md`) — those genuinely require frontmatter to install. If the user picked that path at the Step 0 gate, ignore this rule.
- ❌ Do **not** retro-strip frontmatter from existing skills. Only apply on create, or on an edit the user asked for.

**Consequences to state when you build one:** the skill will not appear in Claude's skills list and will never self-trigger. `/<slug>` (Step CC-6) becomes the *only* way in — so **Step CC-6 is not optional on this path.** A skill with no frontmatter and no slash command is unreachable.

**Verify before done:**
```bash
head -1 "<slug>/skill/SKILL.md" | grep -q '^---$' && echo "FAIL: frontmatter present, strip it" || echo "OK: no frontmatter"
```

---

## Step CC-1 — Find (or create) the Claude Code skills base folder

The base folder is where all Claude Code skills live. Resolve it in this order and use the first that exists:

1. `~/Documents/Claude/Skills` (the standard location — this is where the setup puts it)
2. `~/Library/CloudStorage/Dropbox/Mac/Documents/Claude/Skills` (only if this user syncs their Claude folder through Dropbox)

```bash
BASE=""
for p in "$HOME/Documents/Claude/Skills" \
         "$HOME/Library/CloudStorage/Dropbox/Mac/Documents/Claude/Skills"; do
  [ -d "$p" ] && BASE="$p" && break
done
echo "$BASE"
```

- If neither exists, **ask the user** where their Claude Code skills folder is, or offer to create `~/Documents/Claude/Skills`. Don't guess a random location.
- Windows note: the same folder under the user's Documents (`%USERPROFILE%\Documents\Claude\Skills`). Use forward slashes / `$HOME` equivalents as the environment allows.

---

## Step CC-2 — Name the skill folder (lowercase, dashes for spaces)

The folder name (the "slug") is the skill name, **all lowercase, spaces replaced with dashes**, no other punctuation.

- "Notion Export Cleaner" → `notion-export-cleaner`
- "Q2 Budget Report" → `q2-budget-report`

This slug is used for: the folder name and the slash command file `~/.claude/commands/<slug>.md`. Keep both identical. **There is no `name:` in frontmatter to match — this path has no frontmatter at all (RULE CC-0).**

---

## Step CC-3 — Stamp out the folder from the bundled template

Create the project folder and its three empty subfolders, then copy the three template files **from this skill's own bundled assets** (`<this-skill>/assets/claude-code-template/`). `<this-skill>` is this skill's install/base directory — the folder that contains this `SKILL.md` (given to you as the skill's base directory at load time).

```bash
BASE="<resolved base from CC-1>"
SLUG="<slug from CC-2>"
TPL="<this-skill>/assets/claude-code-template"   # bundled inside THIS skill
DEST="$BASE/$SLUG"

mkdir -p "$DEST/skill" "$DEST/outputs" "$DEST/random"
cp "$TPL/CLAUDE.md"     "$DEST/CLAUDE.md"
cp "$TPL/MEMORY.md"     "$DEST/MEMORY.md"
cp "$TPL/gitignore.txt" "$DEST/.gitignore"   # bundled as gitignore.txt; lands as .gitignore
```

Resulting structure (identical to every other Claude Code skill on the user's machine):

```
<category>/<slug>/
├── CLAUDE.md            ← project instructions (from template, then customized)
├── MEMORY.md            ← skill-specific memory (from template, then customized)
├── .gitignore
├── skill/               ← THE skill goes here (Step CC-5)
├── outputs/             ← per-task work files
└── random/              ← scratch
```

> If `<this-skill>/assets/claude-code-template/` is somehow missing (older install), fall back to the copies described in `assets/claude-code-template/` — do not silently invent different content. The template is the source of truth for these files.

---

## Step CC-4 — Customize CLAUDE.md and MEMORY.md for THIS skill

The copied files are generic and contain placeholders. Replace every placeholder with the new skill's real values (use `Edit`, targeted find/replace):

| Placeholder | Replace with |
|---|---|
| `{Skill Name}` | The skill's human name, e.g. "Notion Export Cleaner" |
| `{skill-name}` | The slug, e.g. `notion-export-cleaner` |
| `{skill purpose}` | One short phrase for what the skill does, e.g. "converting Notion exports to clean Markdown" |
| `YYYY-MM-DD` (in MEMORY.md `Last updated:`) | Today's date — run `TZ='America/New_York' date '+%Y-%m-%d'` |

Do not leave any `{...}` placeholder unfilled. Scan both files for stray `{` after editing.

---

## Step CC-5 — Build the actual skill INSIDE `skill/`

The skill itself lives in the inner `skill/` folder — never at the project root. Build it there following the normal build flow from `new-skill.md`:

- Run the **Step 0D scope gate** (`references/new-skill.md`), then the **Phase 1a interview** (`references/interview.md`) and the **Phase 1b brainstorm** — same as any build. The platform choice skips none of them.
- Write `<slug>/skill/SKILL.md` — **NO YAML frontmatter (RULE CC-0)**. Start with an `# <Skill Name>` heading, then the version line `**Version: v1.0.0** — Full history in [CHANGELOG.md](./CHANGELOG.md).` Skip `references/skill-quality.md` §1 (description writing) entirely on this path — there is no description to write. Its §7 artifact quality gate still applies.
- Write `<slug>/skill/CHANGELOG.md` with the standard preamble + a v1.0.0 row (see `references/changelog.md`).
- Add `<slug>/skill/references/`, `<slug>/skill/scripts/`, `<slug>/skill/tests/evals.json` as needed.

**No `.skill` packaging.** Claude Code reads the files live from disk, so there is nothing to zip and nothing to re-import. Skip `packaging.md` entirely for this path.

**Before calling it done:** Phase 4 tests, Phase 4b functional eval, and Phase 4c prune (`references/phases.md`, `references/prune.md`), then the §7 artifact quality gate in `references/skill-quality.md`.

---

## Step CC-6 — Register the slash command (REQUIRED — it is the ONLY way in)

**Never skip this step.** With no frontmatter (RULE CC-0) the skill cannot self-trigger and does not appear in Claude's skills list. `/<slug>` is the only entry point; without it the skill is unreachable.

Immediately register the skill as a Claude Code slash command so the user can call it with `/<slug>`. Use the **`Write` tool**, never a shell script (shell reads of Dropbox-backed skill folders are frequently TCC-blocked on macOS; `Write` is not).

Silently skip only if `~/.claude/commands/` does not exist (Claude Code isn't set up on this machine).

> ⛔ **Never resurrect a deliberately deleted command.** Before writing, check the denylist in
> `~/.claude/scripts/sync-anthropic-skills-to-commands.sh` (`IGNORE=(...)`). **If `<slug>` is in
> that array, do NOT write the command file** — it was deleted on purpose and the array is what
> keeps it deleted. Say so and move on. Only register a command for a skill you just created, or
> one the user explicitly asked you to (re-)register. **Never bulk-register commands for skills
> you merely found on disk.**

`Write` the file `~/.claude/commands/<slug>.md` with exactly:

```
Use the skill in `<base>/<category>/<slug>/skill/`.

Read that skill's `SKILL.md` first, then apply it to the user's request below.
```

Point it at the **inner `skill/` folder** — that's where `SKILL.md` lives for a Claude Code skill built this way. Then tell the user `/<slug>` is ready (new sessions list it immediately; an already-open session may need a fresh session).

**On a rename or move:** write the new `<new-slug>.md`, delete the old command file, then grep `~/.claude/commands/` and `~/.claude/scheduled-tasks/` for the old path — a sync script only repairs the `Use the skill in \`…\`` pointer, not paths embedded mid-prompt.

---

## Done — what to tell the user

- Where the skill lives: `<base>/<category>/<slug>/` (and the skill files in `<slug>/skill/`).
- How to edit it later: open the files directly and edit — no repackaging.
- The `/<slug>` command is registered.
- No `.skill` file was produced (by design — this is the easy-to-edit path).
