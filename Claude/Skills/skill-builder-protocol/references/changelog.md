# Reference: Changelog Format & Versioning Rules

Load this file whenever writing or updating a changelog.

---

## CHANGELOG.md Format

```markdown
# Changelog — [skill-name]

All notable changes to this skill are documented here.
Format follows semantic versioning: MAJOR.MINOR.PATCH
Date format: `YYYY-MM-DD at H:MM PM EST` (e.g. `2026-04-12 at 9:55 PM EST`)
> ⚠️ **Always run `TZ='America/New_York' date '+%I:%M %p'` before writing any timestamp.** Never guess or estimate the time.

---

## [v1.0.0] — YYYY-MM-DD at H:MM PM EST

### Added
- Initial release — [brief description of what the skill does]
```

---

## Version Line in SKILL.md

Place this immediately after the YAML frontmatter, before any other content. **On the Claude Code path there is no frontmatter** (`references/claude-code-skill.md` RULE CC-0) — put the version line directly under the `# <Skill Name>` heading instead:

```markdown
**Version: v1.X.X** — Full history in [CHANGELOG.md](./CHANGELOG.md).
```

---

## Versioning Rules

| Change Type | Bump |
|-------------|------|
| Minor fix, typo, small wording tweak | `v1.0.0` → `v1.0.1` (PATCH) |
| New feature, new behavior, meaningful structural addition | `v1.0.0` → `v1.1.0` (MINOR) |
| Major restructure or breaking change to how the skill works | `v1.0.0` → `v2.0.0` (MAJOR) |

**Every save = version bump.** If SKILL.md is saved, the version must change and CHANGELOG.md must get a new row.

**Never delete old changelog rows.** Full history must stay in CHANGELOG.md.

**Changelog summaries must be specific** — "Added version history requirement and save-path check" not just "Updated".

---

## Timestamp Rule

Always run this command before writing any timestamp:
```bash
TZ='America/New_York' date '+%Y-%m-%d at %I:%M %p'
```

Never estimate or guess the current time.

---

## Migration: Embedded Changelog → Separate File

If an existing skill has version history embedded in SKILL.md (old format):

1. Create `CHANGELOG.md` in the skill folder
2. Move all history rows there — format each entry as:
   ```markdown
   ## [vX.X.X] — YYYY-MM-DD at H:MM PM EST

   ### Added / Changed / Fixed
   - [description]
   ```
3. Replace the embedded section in SKILL.md with the single version line above
4. Bump the version number for this migration and add a changelog row:
   ```markdown
   ### Changed
   - Migrated version history from SKILL.md into separate CHANGELOG.md
   ```

If no version info exists at all: create both the version line and CHANGELOG.md starting at v1.0.0, then add the current update as the next increment.

---

## New Changelog Row Format

Each entry goes at the **top** of the changelog (newest first), below the header block:

```markdown
## [v1.X.X] — 2026-04-12 at 11:47 PM EST

### Added
- [What was added]

### Changed
- [What was changed]

### Fixed
- [What was fixed]
```

Use only the sections that apply. Omit empty sections.
