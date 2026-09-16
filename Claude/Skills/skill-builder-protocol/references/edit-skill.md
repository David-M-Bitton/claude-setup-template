# Reference: Editing an Existing Skill

Load this file when **making changes to an existing skill** — corrections, additions, fixes, refactors, reviews, or "make this smaller".

**An edit session is also a cleanup session.** Every edit runs the Upgrade Pass below, which brings the existing skill up to the current standards — not just the one change the user asked for.

---

## Step 0A — Confirm Save Paths FIRST

**One home for this rule: `SKILL.md` → "Always: Confirm Save Paths First".** Follow it there, including the Claude Code carve-out. Don't re-derive it from this file.

By the time you are reading `edit-skill.md`, Step 0A should already be done.

---

## Step 0B — Path Reality Check (Cowork path only)

**Claude Code path: skip this entire section.** The skill folder on the user's Mac is directly writable — edit it in place and move on to the Upgrade Pass. Everything below applies only to a Cowork-installed skill you are editing inside a `/sessions/<session>/mnt/` mount.

**Editing a live Cowork skill is path-hostile by default.** Before touching any file, you must figure out where you can actually write. Older docs assumed a `request_cowork_directory` call on the skill folder that **frequently fails because the path is protected**. Don't burn 5+ tool calls rediscovering this every session.

### The 4 places a skill might live (and which are writable)

| Path pattern | Writable? | Notes |
|---|---|---|
| `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/.../skills/<skill>` | ❌ Protected — `request_cowork_directory` REJECTS this. Don't try it. | "overlaps a protected host location" error |
| `/var/folders/.../claude-hostloop-plugins/.../skills/<skill>` | ❌ Outside session — file tools error with "outside this session's connected folders" | This is the live plugin cache mount used at runtime |
| `/sessions/<session>/mnt/.claude/skills/<skill>` | ❌ **Read-only** (mode `r--`) | Source of truth to copy FROM, never write to |
| `/sessions/<session>/mnt/<user-mounted-folder>/<skill>` | ✅ Writable, persists to user's Mac | The ONLY reliable write target |

### The 30-second path resolution flow — DO THIS FIRST

```
1. ls /sessions/*/mnt/                      # see what folders are mounted
2. If a folder named "copywriting", "Tasks", "Documents", or similar is present → that's the workspace
3. mkdir -p /sessions/<session>/mnt/<workspace>/<skill-name>
4. cp -r /sessions/<session>/mnt/.claude/skills/<skill-name>/. /sessions/<session>/mnt/<workspace>/<skill-name>/
5. chmod -R u+w /sessions/<session>/mnt/<workspace>/<skill-name>/
6. Now Edit / Write directly inside that path
```

### If no writable workspace folder is mounted

Call `request_cowork_directory` with the user's general workspace path (e.g. `~/Documents`, `~/Desktop`, `~/Downloads`), NOT the skill folder itself. Then proceed as above.

**DO NOT** call `request_cowork_directory` with any of these — they will always fail:
- `~/Library/Application Support/...` (protected)
- `/var/folders/...` (sandbox-only)
- Any path the user did not explicitly choose

---

> **VM path reality:** Despite what older docs claim, neither `mnt/skills/` nor the skills-plugin Mac path is reliably writable. Always copy the skill into the user's mounted workspace folder first (see "30-second path resolution flow" above) and edit there. Repackage and present the `.skill` so the user can install the updated version.

---

## File Permissions Gotcha — chmod After Every Copy

When you `cp -r` from `mnt/.claude/skills/<skill>/` (read-only, mode `r--`) into a writable folder, the copies inherit the read-only mode and `Edit` / `Write` will fail with permission errors.

**Always run `chmod -R u+w <dest>` immediately after copying.** This is non-negotiable. If you skip it, the first Edit will fail and you'll waste a turn debugging it.

```bash
cp -r /sessions/<session>/mnt/.claude/skills/<skill>/. /sessions/<session>/mnt/<workspace>/<skill>/
chmod -R u+w /sessions/<session>/mnt/<workspace>/<skill>/
```

If `cp` itself fails on a subfolder with "Permission denied" (the destination already exists with read-only mode from a prior run), `chmod -R u+w` the destination first, then re-run `cp -rn` (no-clobber) to fill in the gaps.

---

## The Upgrade Pass — Run on EVERY Edit (REQUIRED)

Skills built before a standard existed don't meet it. Before making the user's requested change, audit the existing skill against the eight checks below — check 8 splits into 8a and 8b, which get separate verdicts — report what you found, and get approval. **Never apply the whole list silently** — the user may have deliberate reasons for what's there.

**Run check 1 against the requested change as well, not only the existing skill.** A change can be a second job bolted onto a one-job skill; if it is, say so at the gate and offer the split. Auditing only what's already there approves the scope creep and flags it on the next edit instead.

Read the skill's SKILL.md and list its reference files first. **Then also read the skill's `MEMORY.md` — usually at the project root, not inside `skill/`; read whichever levels exist — and every `CLAUDE.md` in the skill folder, then grep the whole skill folder for `mcp__`, connector names, and tool calls.** Some skills have one `CLAUDE.md` at the project root and a second inside `skill/`; **if a second one exists**, the duplication between them is an 8b finding. A single `CLAUDE.md` is normal — don't manufacture a finding out of its absence. A connector documented only in `MEMORY.md` is invisible to the loaded SKILL.md — that gap is itself a check 6 failure, and reading SKILL.md alone will never surface it. Then run each check and report **pass** or the specific problem found.

**Load each check's Reference file at the moment you run that check.** The Reference column is not decoration — the actual standard lives in that file, and the one-line summary in the table is too thin to judge against. Running checks 1–8 in numeric order pulls in `new-skill.md` Step 0D (check 1), `skill-quality.md` §4, §1, §3 (checks 2–4), `prune.md` §1–2 (check 5), `connectors.md` (check 6), then back to `skill-quality.md` §5 (check 7) and §6 (check 8a), and `prune.md` §3 (check 8b) — each opened at its own check. Do not batch them upfront, and do not skip them and grade from the table alone. `interview.md`, `phases.md`, `changelog.md`, `packaging.md`, and `claude-code-skill.md` are **not** part of the audit — they belong to later steps.

| # | Check | Standard | Reference |
|---|---|---|---|
| 1 | **Scope** | One job, statable in one "[verb] [object]" sentence. If the sentence needs "and", propose a split into a chain of smaller skills | `new-skill.md` Step 0D |
| 2 | **Invocation mode** | `disable-model-invocation: true` unless the skill genuinely needs to auto-fire | `skill-quality.md` §4 |
| 3 | **Description** | Two sentences, capability first, explicit `Use when [triggers]`. Rules living in the description move to the body | `skill-quality.md` §1 |
| 4 | **Size and progressive disclosure** | 500 lines is the hard ceiling; ~100–200 is typical. **Shorter is never the defect — do not fail a lean SKILL.md for being under the band.** Every step names the one file it needs, loaded at that step. References one level deep | `skill-quality.md` §3 |
| 5 | **Steps are instructions** | Each step says what to do. No preamble, no rationale, no filler. **No personal names anywhere in the skill body or its reference files — write "the user"**; check 3 catches this only in the description | `prune.md` §1–2 |
| 6 | **Connectors** | Every connector the skill actually uses is named in SKILL.md, not only in MEMORY.md. Static data in a reference file; live calls behind a subagent, with the expected return shape stated in the step | `connectors.md` |
| 7 | **Human-in-the-loop** | A checkpoint before any send/publish/spend/delete. Plus 3–5 concrete options at every **authoring** design choice — a fork you put to the user while building or editing the skill. **This does not govern the advice the finished skill gives.** A skill instructed to answer with one firm recommendation instead of a menu is honoring its author's intent, not failing check 7 — don't score it as a fail. **If the skill uses a connector that exposes write, bulk-edit, or delete tools, the absence of a read-only-by-default or confirm-before-write rule inside the skill is a fail** — a read-only posture stated only in a shared memory hub outside the skill does not count | `skill-quality.md` §5 |
| 8a | **Self-improvement** | Rule embedded, and the files it points at actually exist on disk — open them and confirm. **Then confirm every other file path referenced anywhere in the skill resolves on disk too** — dead pointers hide in `CLAUDE.md` and `MEMORY.md`, not just in the self-improvement rule | `skill-quality.md` §6 |
| 8b | **Duplication** | Every rule has exactly one home. Check across SKILL.md, both `CLAUDE.md` files, and `MEMORY.md` — a rule restated in three places is three things to keep in sync | `prune.md` §3 |

Then:

1. **Present the findings** as a short list — what passes, what doesn't, and the one-line fix for each.
2. **Ask:** "Apply all of these along with your change, or just some?" **Wait for the answer.**
3. **Apply** what they approved, plus the change they originally asked for.
4. **Run the prune pass** (`references/prune.md`) and report line count before → after.
5. **Run the functional eval** (`references/phases.md` Phase 4b) if behavior changed.
6. **Complete the Sync Checklist** below.

If the user declines a fix, add a one-line note under a `## Known Gaps` heading in that skill's SKILL.md, so the next session doesn't re-litigate the same finding.

**For a review-only request** ("review this skill", "why does this skill suck", "make it smaller"): run checks 1–8, deliver the findings, and stop. Don't edit until the user picks what to apply.

---

## Sync Checklist After Every Change

After **every** instruction — a correction, addition, clarification, or fix — complete this checklist before moving on:

- [ ] SKILL.md updated to reflect the change
- [ ] **Version number bumped in SKILL.md**
- [ ] **New changelog row added to CHANGELOG.md**
- [ ] Any affected tests updated
- [ ] Troubleshooting notes added if the change was prompted by a failure
- [ ] Frontmatter `description` updated if triggering behavior changed — and if you touched it, self-check it against `references/skill-quality.md` §1: capability-first, explicit `Use when [triggers]` clause, third person, ≤1024 chars, no personal names. **Claude Code path: N/A — no frontmatter exists (`references/claude-code-skill.md` RULE CC-0). Never add one back. Do not retro-strip frontmatter from an existing skill unless the user asked.**
- [ ] Upgrade Pass findings reported and the approved fixes applied
- [ ] Prune pass run, line count before → after reported (`references/prune.md`)
- [ ] **Cowork-installed skills only: repackage as `.skill` and present to the user** (see `references/packaging.md`). Claude Code skills are read live from disk — nothing to repackage
- [ ] **On a rename:** write the new `~/.claude/commands/<new-slug>.md`, delete the old command file, and grep `~/.claude/commands/` and `~/.claude/scheduled-tasks/` for the old path (`references/claude-code-skill.md` CC-6)

The skill must always reflect the current agreed-upon behavior. If a future Claude reads only SKILL.md with no chat history, it must behave correctly.

> ⚠️ **Why repackaging is mandatory — Cowork-installed skills only:** The Claude desktop app reads from the installed `.skill` package — not from the raw files on disk. If you update the files but don't repackage and present the `.skill`, the user's installed skill will be out of date and they won't see the changes. End every **Cowork** edit session by repackaging and presenting the `.skill` so the user can install it. **On the Claude Code path there is nothing to repackage** — the skill is read live from the folder on disk. Don't zip it.

---

## Version Bump Rules

Use semantic versioning:
- `v1.0.1` → minor fix, typo, or small wording tweak
- `v1.1.0` → new feature, new behavior, or meaningful structural addition
- `v2.0.0` → major restructure or breaking change to how the skill works

**Every save = version bump.** If SKILL.md is saved, the version must change and CHANGELOG.md must get a new row.

---

## Changelog Migration (if needed)

If the existing skill still has version history embedded in SKILL.md (old format):
1. Create `CHANGELOG.md` in the skill folder
2. Move all history rows there
3. Replace the embedded table in SKILL.md with a single version line:
   ```markdown
   **Version: v1.X.X** — Full history in [CHANGELOG.md](./CHANGELOG.md).
   ```

If no version info exists at all: create both the version line and CHANGELOG.md starting at v1.0.0, then add the current update as the next increment.

---

## Large Edits — Run the Interview First

For any edit that involves significant restructuring, new phases, new reference files, or behavioral changes that affect how Claude uses the skill — run the interview in `references/interview.md` before writing anything.

**Order is fixed: Upgrade Pass → approval gate → interview → write.** Never interview before the audit. The audit tells the user what's broken; the interview shapes what you build with their answers. Running it first delays the findings and lets the requested change get designed around problems you haven't reported yet.

Scope it to the edit — you already have a working skill, so skip the big-picture questions and interview only the new behavior: what triggers it, what it returns, what happens when it fails.

---

## Edit Efficiency Rules

- **Prefer `Edit` over `Write`**: Use targeted Edit (find-and-replace) for changes to existing files — it only sends the diff and is far more token-efficient.
- Only use `Write` (full file rewrite) when replacing the majority of a file's content.
- When updating changelogs or appending content, use `Edit` to prepend or insert — not a full rewrite.
