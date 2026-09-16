# Changelog — skill-builder-protocol

All notable changes to this skill are documented here.
Format follows semantic versioning: MAJOR.MINOR.PATCH
Date format: `YYYY-MM-DD at H:MM PM EST` (e.g. `2026-04-12 at 9:55 PM EST`)

---

## Bundle copy — adapted for the setup template

> This folder is the **setup-template copy** of the skill, synced from the maintained original at
> v1.23.0. It is functionally identical; only paths and folder conventions differ, because a
> freshly set-up machine has a flat skills folder and no category folders.
>
> **What was changed when syncing (re-apply these after any future sync):**
> - Skills base is `~/Documents/Claude/Skills` (Dropbox path kept only as a fallback), not `.../Claude/Skills`.
> - **Step CC-1b (ASK which category folder) was removed entirely**, along with `$CATEGORY`; skills go directly in `$BASE/$SLUG`. The template ships no `generic-skills` / `personal-skills` / `work-skills` folders.
> - `references/new-skill.md` Step 0-folder reduced to a pointer, for the same reason.
> - Routines pointer is `~/Documents/Claude/Memory/routines.md` (the template's Memory folder is flat, with no `Efficiency/` subfolder).
> - Personal references removed: "David" → "the user", "Second Brain" → the `Context/` knowledge base.
>
> **Do not reintroduce `ai-file-manager`.** It was merged into this skill in v1.23.0 below and no
> longer exists. Two assertions in `tests/evals.json` guard against it.

---

## [v1.23.0] — 2026-08-11 at 9:04 PM EST

### Removed
- **The `ai-file-manager` dependency is gone.** That skill's four jobs all had live homes elsewhere, and where they disagreed, ai-file-manager was the stale side: (1) its migration scan was already restated in full in this `SKILL.md`; (2) its `request_cowork_directory`-on-the-skill-folder rule is contradicted by `references/edit-skill.md` Step 0B, which documents that call failing on a protected path; (3) its packaging rule ("workspace folder only, one link, never copy to outputs") contradicts `references/packaging.md` ("copy to both, surface the outputs link"); (4) its scheduled-task rule (prompt = `"Run the <name> skill."`, README to `Claude/Scheduled/<task-id>/`) is superseded by `Memory/Efficiency/routines.md`, whose ONE RULE makes the prompt a one-line pointer to a spec file. Its own `tests/evals.json` still asserted the retired `Claude/Skills/` path and `present_files`, which `packaging.md` records as always failing. Adding a reference file here would have been a fifth copy, so the content was absorbed and the skill retired instead.

### Changed
- **`SKILL.md` — "Always: Use ai-file-manager First" → "Always: Confirm Save Paths First".** Now fully self-contained and skill-agnostic. Keeps the migration scan verbatim, absorbs the three facts Step 0A used to extract from ai-file-manager (base directory, kebab-case folder naming, category-folder placement with "never guess — ask"), and routes the Cowork half to `references/edit-skill.md` Step 0B + `references/packaging.md` rather than describing it. Adds a pointer to `Memory/Efficiency/routines.md` for any session that also wires up a scheduled routine — explicitly out of scope for this skill.
- **`references/new-skill.md` Step 0A — collapsed from 24 lines to a 3-line pointer** at `SKILL.md`, matching the shape `references/edit-skill.md` Step 0A already had. It carried its own stale VM-path note and an "extract from ai-file-manager" list that named facts `SKILL.md` now states directly. Step 0's opening line reworded.
- **`references/edit-skill.md`** — Step 0A heading and pointer retitled; Step 0B's "documented in older versions of ai-file-manager" reworded to "older docs" so the warning survives the skill's removal.
- **`references/changelog.md`** — the specificity example no longer cites an ai-file-manager check.
- **`tests/evals.json`** — `file-manager-001` and `ai-file-manager-claude-code-scope-001` (renamed `save-paths-claude-code-scope-001`) rewritten to assert the in-file save-path section. The renamed eval gains an assertion that no separate ai-file-manager skill is invoked, so a future session can't reintroduce the dependency silently.

### Notes
- The `/ai-file-manager` slash command was removed. The skill folder itself is the user's to delete.

---

## [v1.22.0] — 2026-08-07 at 10:31 AM EST

### Added
- **RULE CC-0 in `references/claude-code-skill.md`: a Claude Code `SKILL.md` NEVER gets YAML frontmatter.** No `---` block, no `name:`, no `description:`. The file opens with an `# <Skill Name>` heading, then the version line. Reason: the frontmatter `description` is the auto-trigger surface — Claude reads it at startup and fires the skill on its own judgement. These skills must fire **only** when the user types `/<slug>`. Frontmatter also costs startup-menu tokens every session whether the skill is used or not. Includes DO/DON'T blocks, scope carve-outs, and a `head -1 | grep '^---$'` verify command.
- Routing-table row in `SKILL.md` pointing at RULE CC-0.

### Changed
- **Step CC-5 — reversed.** Previously instructed "YAML frontmatter (`name: <slug>`, description per `references/skill-quality.md`)". Now mandates no frontmatter and skips `skill-quality.md` §1 on this path.
- **Step CC-2** — dropped `name:` in frontmatter from the "keep all three identical" rule; the slug now maps to the folder name and the command file only.
- **Step CC-6** — retitled "REQUIRED — it is the ONLY way in". With no frontmatter the skill cannot self-trigger and is unreachable without the slash command, so skipping CC-6 now breaks the skill rather than merely inconveniencing the user.
- **`references/skill-quality.md` §1** — added a stop banner: skip the whole section on the Claude Code path. §7 artifact gate still applies to both paths.
- **`references/new-skill.md`** Step 0B and the structural-conventions list — frontmatter marked packaged/Cowork-only, with the Claude Code exception and version-line placement under the `#` heading.
- **`references/changelog.md`** — version-line placement rule now covers the no-frontmatter case.
- **`references/edit-skill.md`** checklist — frontmatter-description item marked N/A on the Claude Code path, plus explicit "never add one back" and "do not retro-strip existing skills unless asked".

- **Step CC-6 — added a denylist guard.** Before writing `~/.claude/commands/<slug>.md`, check the `IGNORE=(...)` array in `~/.claude/scripts/sync-anthropic-skills-to-commands.sh`; if the slug is listed, do not write the file. Plus: never bulk-register commands for skills merely found on disk. Reason: 17 old commands were deleted 2026-08-07 and any blind re-registration undoes that.

### Notes
- The packaged / Cowork `.skill` path is **unchanged** — it still requires frontmatter to install.
- No existing skill was modified. The rule applies on create, and on edits the user requests.

---

## [v1.21.0] — 2026-08-03 at 5:35 PM EST

Third Phase 4b functional eval against `personal-finance` (3 parallel dry runs, fresh contexts, same input as v1.18.0). **All three criteria passed 3/3** — order (ai-file-manager first → `edit-skill.md` → full audit before the requested change → stop at the gate with the verbatim question, zero writes), progressive disclosure (all five expected references loaded, each at its own check, `new-skill.md` read as a ~20-line slice; none of the four forbidden files opened by any run), and Upgrade Pass completeness (8/8 checks scored, check 6 producing its real finding 3/3). The v1.18.0 reference-loading fix held — the under-load failure it was written for did not recur.

The defects below came from where the three runs **disagreed**: checks 1, 2, and 4 got different verdicts on the same skill from three faithful runs. Each fix removes the ambiguity that allowed the split.

### Fixed
- **SKILL.md — the inline upgrade-pass summary named the wrong checks.** It listed "scope, invocation mode, progressive disclosure, connectors, human-in-the-loop options, self-improvement rule, prune, functional eval": omitting **description**, **steps-are-instructions**, and **duplication**, and padding with prune + functional eval, which are post-approval steps. A session that read SKILL.md and skimmed `edit-skill.md` ran a materially different audit and never checked the description — the violation SKILL.md's own non-negotiables line calls out. Now names all eight checks, points to `edit-skill.md` as authoritative, and states that prune and the functional eval come after the gate. Found by 3 of 3 runs.
- **`references/edit-skill.md` — the reference load map stopped at check 6.** It enumerated loads through `connectors.md` and never said checks 7 and 8a return to `skill-quality.md` (§5, §6) and 8b to `prune.md` (§3), implying those checks need no reference file. Now maps all eight, with the section anchor for each. Standardized "§0D" to "Step 0D" to match the table.
- **`references/skill-quality.md` §3 — "references one level deep" was unfalsifiable.** Nothing said how to test it, so two runs eyeballed it and passed check 4 while the third grepped, found 50+ reference-to-reference links, and failed it. Now specifies `grep -rn '](.*\.md)' references/` and how to read the result.
- **`references/edit-skill.md` check 5 — the no-personal-names rule had no enforcer.** SKILL.md declares it non-negotiable, but only check 3 tested it, and only inside the description. A skill with names throughout its body passed all eight checks. Check 5 now covers the body and reference files.
- **`references/edit-skill.md` check 8a — on-disk verification was scoped to the self-improvement rule's targets only.** All three runs found the same dead pointer (a `config.json` cited in the target's `CLAUDE.md` that doesn't exist) purely as a side effect. Now requires every referenced path in the skill to resolve.
- **SKILL.md — the migration scan didn't define a stale copy.** Each run improvised a criterion. Now stated: any loose `SKILL.md` or `.skill` not inside a named skill subfolder, or a duplicate slug folder.

### Changed
- **`references/skill-quality.md` §4 — a fourth auto-fire question, and no more soft verdicts.** Runs split 2-fail/1-weak-pass on check 2 because a knowledge-base skill whose value is grounding answers in the user's private data fit none of the three questions cleanly. Added that case, and check 2 now demands a hard pass or fail: a pass names which question it satisfies, no yes is a fail.
- **`references/edit-skill.md` — check 1 now runs against the requested change, not only the existing skill.** One run caught that "flag uncategorized transactions over $500" is a live-data monitoring job bolted onto a knowledge-base skill; the other two didn't, because nothing asked them to. The protocol was approving scope creep and flagging it on the next edit.
- **SKILL.md — the ai-file-manager invocation is now skippable on the Claude Code path.** All three runs loaded a Cowork-shaped file to extract two facts that SKILL.md already states in full, and its Initialization block carries `mkdir -p` side effects outside the carve-out. The Cowork path is unchanged.

### Added
- **6 evals**, one per finding: authoritative check list, reference loading at checks 7–8b, check 1 on the requested change, grep-verified nesting, personal names + dead pointers, and hard invocation-mode verdicts. 36 → 42 tests.

---

## [v1.21.0] — 2026-08-03 at 6:20 PM EST

### Removed
- **`references/resolver-check.md`, Phase 4d, and the `/resolver-check` command — reverted, one version after they were added.** The check was built on a premise that does not hold in this workspace: it audited each skill's `SKILL.md` `description` as the trigger surface. It isn't. Local folder skills reach Claude through their `~/.claude/commands/<name>.md` wrapper, and **48 of 56 of those wrappers are bare pointers with no description at all** — so they cannot collide on description, and the MECE half of the check had nothing to act on. The DRY half (don't build a skill you already have) is real but does not need a reference file, a phase, and a slash command; it is one line. Its 2 evals were removed with it.
- **`references/learn-from-transcript.md`** — removed in the same session it was added, before shipping. The useful half runs automatically in the dream-cycle routine instead.

### Changed
- **SKILL.md Phase 0D now carries the surviving rule in one line:** "List the existing skills first and confirm this isn't one of them." That is the whole of what the resolver check was worth here.
- **`MEMORY.md` and project `CLAUDE.md`** — resolver-check references stripped from the non-negotiables, the folder map, and the core-memory list.

### Kept from v1.20.0
- **`scripts/session_turns.py`** stays. It is used by the nightly dream-cycle routine and is useful on its own for "what did I correct this week?"

---

## [v1.20.0] — 2026-08-03 at 4:40 PM EST

Three additions from the YC internal-agent architecture described in "Inside YC's AI Playbook" (The Lightcone, 2026-05-27). Notes and trust check: `../../youtube-summarizer/outputs/2026-08-03 - Inside YCs AI Playbook.md`.

### Added
- **`references/resolver-check.md` — a new Phase 4d, the resolver check.** `prune.md` §3 enforced one home per rule *inside* a skill; nothing checked *across* skills, so overlap accumulated invisibly. The check treats the skill registry as a lookup table and scores every close pair on **DRY** (same job?) and **MECE** (could one request match both?). **The load-bearing point: the `description` is the resolver, not the body** — two skills with unrelated bodies still collide when their trigger phrases overlap, which is the most common real defect and usually a one-sentence fix. Four verdicts (merge / parameterize / disambiguate / leave), a "what is NOT a finding" list so the check doesn't manufacture work, report-never-auto-apply, and the `sync-skill-commands.py` + grep step that a merge or delete requires. Runs on every new or renamed skill; library-wide sweep on request. Findings log to `outputs/`, so repeat sweeps skip anything already ruled `LEAVE`.
- **`references/learn-from-transcript.md` — improve a skill from an artifact instead of by hand.** Feed the skill a recording, a worked example plus its feedback, or a session where the user corrected the output repeatedly; extract only what **contradicts or extends** the skill and discard what merely confirms it. Includes the traps: style is not a rule (would the opposite have been *wrong*, or just different?), twice-means-a-rule, verify proper nouns and numbers from machine transcripts, and route standing behaviour rules to the relevant `CLAUDE.md` rather than smuggling them into a skill body.
- **`scripts/session_turns.py`** — prints only the human turns from recent Claude Code session logs (`~/.claude/projects/**/*.jsonl`), skipping assistant output and tool results. `python3 scripts/session_turns.py 7 --stats` for counts first. Read-only. Verified against 119 sessions / 344 turns.

### Changed
- **SKILL.md** — version to v1.20.0; resolver check added to the session non-negotiables; two new rows in the Start Here table (transcript-driven improvement, library sweep) and two in the reference-routing table; Phase 4d added to the phase table.
- **Project `CLAUDE.md`** — resolver check added to the non-negotiables line; folder map now shows `references/` covering the two new playbooks and the new `scripts/` entry.
- **`MEMORY.md`** — **its version line was stale at v1.17.0 while the skill was on v1.19.0.** Corrected to v1.20.0 with a note not to trust it over the CHANGELOG, plus entries for Phase 4d, transcript learning, and the nightly dream cycle.

### Related, outside this skill
- **`~/.claude/scheduled-tasks/skills-dream-cycle-nightly/`** — runs `scripts/session_turns.py` nightly, routes each finding to the narrowest file that fits, and writes a dated proposals file to this skill's `outputs/`. **It proposes and never applies** — same policy as `second-brain-optimizer-monthly`.

---

## [v1.19.0] — 2026-08-03 at 2:57 PM EST

Fixes from two Phase 4b functional evals (3 parallel dry runs each) against `personal-finance` and `amazon-product-finder`. Both eval sets passed on order, progressive disclosure, and Upgrade Pass completeness; these are the protocol defects the 6 runs surfaced.

### Fixed
- **`references/edit-skill.md` — reference load order corrected.** It listed `connectors.md` before `prune.md` "in that order", but `prune.md` is check 5 and `connectors.md` is check 6. Now states numeric order with each check named: `new-skill.md` §0D (1), `skill-quality.md` (2–4), `prune.md` (5), `connectors.md` (6). Found by 4 of 6 runs.
- **`references/edit-skill.md` — the second `CLAUDE.md` is no longer presumed.** "There is usually one at the project root and a second inside `skill/`" primed a duplication finding in skills that have only one. Now conditional, with an explicit "a single `CLAUDE.md` is normal — don't manufacture a finding out of its absence."
- **`references/edit-skill.md` — `MEMORY.md` level disambiguated.** "The skill's `MEMORY.md`" didn't say project root vs `skill/`. Now says project root is the usual home; read whichever levels exist.
- **`references/edit-skill.md` Step 0A — collapsed to a pointer.** It restated the ai-file-manager rule with no Claude Code carve-out and listed only Cowork scan paths (`/sessions/*/mnt/`, `mnt/skills/`) that don't exist on a Mac folder, disagreeing with the carve-out in SKILL.md. Two homes for one rule, violating this protocol's own `prune.md` §3. SKILL.md is now the single home and absorbs the migration-scan paths.
- **`references/edit-skill.md` — repackaging callout no longer contradicts the checklist above it.** The Sync Checklist correctly carved out Claude Code ("read live from disk — nothing to repackage"); the warning box then said "Always end every edit session by repackaging" with no qualifier. Now scoped to Cowork, with an explicit "don't zip it" for Claude Code.

### Changed
- **`references/edit-skill.md` — check 7 now covers connector write surfaces.** A skill wired to a connector exposing write, bulk-edit, or delete tools fails check 7 if no read-only-by-default or confirm-before-write rule lives *inside the skill*; a read-only posture stated only in a shared memory hub doesn't count. Added because 3 runs against the same connector-backed skill split 2-fail/1-pass on exactly this ambiguity. The existing carve-out (one firm recommendation ≠ a menu failure) is unchanged.
- **SKILL.md routing table — the edit row now says to load `references/edit-skill.md` before reading any file in the target skill.** 2 of 3 runs read the target's SKILL.md, MEMORY.md, and both CLAUDE.md files *before* opening the file that tells them what to read.

---

## [v1.18.0] — 2026-08-03 at 6:45 PM EST

### Changed
- **`references/edit-skill.md` — the Upgrade Pass now says to LOAD each check's Reference file at that check.** The table has always had a Reference column, but nothing instructed the auditor to open it, and SKILL.md's "load only the reference file the current step names — never all of them" reads as a prohibition. Added an explicit paragraph: checks 1–8 pull in `new-skill.md` §0D, `skill-quality.md`, `connectors.md`, and `prune.md`, each opened at its own check, never batched upfront — and `interview.md`, `phases.md`, `changelog.md`, `packaging.md`, `claude-code-skill.md` are explicitly *not* part of the audit.
- **`references/edit-skill.md` — check 7 scoped to authoring decisions only.** The "3–5 concrete options at every design choice" standard now states it governs forks put to the user *while building or editing a skill*, not the advice the finished skill gives its own user. A skill instructed to answer with one firm recommendation is honoring its author's intent, not failing check 7.
- **`references/edit-skill.md` — check 8 split into 8a (self-improvement) and 8b (duplication)** with separate verdicts and separate reference pointers. Still eight checks. 8b now names both `CLAUDE.md` files and `MEMORY.md` as part of the duplication surface.
- **`references/edit-skill.md` — check 4 reworded so short is never a failure.** "~100–200 lines (500 hard ceiling)" read as a floor. Now: 500 is the ceiling, ~100–200 is typical, and a lean SKILL.md must not be failed for being under the band.
- **`references/edit-skill.md` — audit scope says every `CLAUDE.md`, not "the skill's `CLAUDE.md`".** Skills routinely have two (project root + `skill/`); the singular wording under-specified it, and the duplication between them is itself an 8b finding.
- **SKILL.md — ai-file-manager scoped for the Claude Code path.** Run only the migration scan and save-path confirmation; `request_cowork_directory`, `mnt/` mounts, `.skill` packaging, and `computer://` links do not apply to a directly-writable folder on the user's Mac. Matches the Step 0B carve-out that already existed in `references/edit-skill.md`.
- **`CLAUDE.md` §Output workflow — the `outputs/` file moved from step 2 to step 4**, after the approval gate. It previously ordered a write *before* the work, contradicting the Upgrade Pass rule that nothing is written until the user answers the gate question.

### Added
- **4 evals** covering each finding: reference-loading at the right check, check 7 authoring-vs-advice, check 4 leanness, and ai-file-manager's Claude Code scope. 29 → 33 tests.

### Why
Phase 4b functional eval, 3 parallel subagents, fresh contexts, dry run, against "add a step to my personal-finance skill that flags any transaction over $500 that isn't categorized yet." **Order passed 3/3** — ai-file-manager first, route to `edit-skill.md`, full audit before the requested change, stop at the gate with the verbatim question, zero writes. **Check 6 produced its real finding 3/3** — personal-finance's Monarch MCP appears only at its `MEMORY.md:31` and zero times in its 65-line SKILL.md, with no subagent wrapper and no stated return shape; the v1.17.0 grep instruction held. **Reference loading failed 3/3, and in the under-load direction**: nobody loaded a forbidden file, but two of three runs graded all eight checks without ever opening `skill-quality.md` or `connectors.md`, and *no* run opened `prune.md` or `new-skill.md`. The audit was being scored off one-line table summaries. Runs disagreed only on checks 5 and 7, both traced to soft wording now tightened.

---

## [v1.17.0] — 2026-08-03 at 4:20 PM EST

### Changed
- **`references/edit-skill.md` — Upgrade Pass audit scope widened.** "Read the skill's SKILL.md and list its reference files" now also requires reading the target skill's `MEMORY.md` and `CLAUDE.md` and grepping the folder for `mcp__`, connector names, and tool calls. A connector documented only in `MEMORY.md` is invisible to the loaded SKILL.md, and reading SKILL.md alone will never surface it — that gap is now itself a check 6 failure.
- **`references/edit-skill.md` — check 6 standard rewritten.** Now reads: every connector the skill actually uses is named in SKILL.md, not only in MEMORY.md; static data in a reference file; live calls behind a subagent **with the expected return shape stated in the step**. The old wording didn't prompt the auditor to ask whether the connector was mentioned at all.
- **`references/edit-skill.md` — Step 0A (ai-file-manager) moved above the path reality check**, which is now Step 0B and explicitly gated "Cowork path only — on Claude Code the folder is directly writable, skip this section." Previously the path check sat first, contradicting SKILL.md's "ai-file-manager before anything else" and putting ~33 lines of Cowork mount detail in front of every Claude Code edit session.
- **SKILL.md — ai-file-manager trigger made unconditional.** "before any file touches disk" → "before anything else in the session, including a read-only review." The old wording was conditional and a review-only session could skip it.
- **`references/interview.md` rule 2 rewritten as "Look facts up; only ask about decisions"** (from grill-me). Fact lookup now spans filesystem, docs, tools, and connectors — not just the session's workspace folder. Added an explicit no-act gate after the recap: no building, no file edits, no execution mid-interview.

### Removed
- **`superpowers:brainstorming` dependency, everywhere.** Replaced with this skill's own interview (`references/interview.md`) in SKILL.md, `references/edit-skill.md`, and `references/new-skill.md` Phase 1b. The plugin was an external dependency for a step this skill already owns, and SKILL.md's unbounded "for large edits" trigger could pull an executor into a brainstorm *before* the Upgrade Pass, breaking audit-first ordering. The order is now fixed and stated: **Upgrade Pass → approval gate → interview → write.**

### Why
Phase 4b functional eval, 3 parallel subagents against the input "add a step to my personal-finance skill that flags any transaction over $500 that isn't categorized." All 3 passed all 3 axes and agreed with each other. The load-bearing failure they found: check 6 produced its real finding (personal-finance's Monarch connector appears zero times in its SKILL.md) only because one run ran an **uninstructed** grep — a literal executor following the audit-scope line as written would have scored check 6 a generic pass. That line was the difference between check 6 being reliable and being luck. The remaining fixes are hardening.

---

## [v1.16.0] — 2026-08-03 at 11:58 AM EST

### Added
- **`references/prune.md` (new) — Phase 4c prune pass.** The deletion test ("if removing it wouldn't change what the agent does, delete it"), no-op detection, one-home-per-rule, sediment clearing, bloat stripping, and a checklist. Required before shipping any skill, new or edited. Reports line count before → after.
- **`references/connectors.md` (new) — connector, MCP, and subagent policy.** Decision ladder: no connector (static data → reference file) > connector behind a subagent > tight-scoped skill. Includes the subagent allow/deny table that **supersedes the old blanket "no subagents" rule**.
- **`references/edit-skill.md` — the Upgrade Pass, required on EVERY edit.** Eight checks (scope, invocation mode, description, size/progressive disclosure, steps-are-instructions, connectors, human-in-the-loop options, self-improvement/duplication) run against the existing skill before the user's requested change. Report findings → ask "all of these or just some?" → apply approved fixes + the change → prune → functional eval → sync checklist. Declined fixes get logged under `## Known Gaps` so the next session doesn't re-litigate. Review-only requests stop at the findings.
- **`references/new-skill.md` — Step 0D scope gate** before the interview: is a skill worth building, name the job in one "[verb] [object]" sentence, the "and" test, right-size to the smallest valuable slice, ship-small-then-iterate. Confirmed with the user before Phase 1a.
- **`references/phases.md` — Phase 4b functional eval** (fresh session, 3 parallel subagents checking step order / on-demand reference loading / correct connector use) and **Phase 4c prune**. Build summary now reports both results.
- **`references/skill-quality.md` §4 invocation mode** — `disable-model-invocation: true` is the default for new skills; auto-invocation only when hands-free triggering beats the standing per-request context cost. **§5 human-in-the-loop** — checkpoints before consequential actions, plus **3–5 concrete numbered options at every design choice**, written into the step. **§6 embedded self-improvement rule** — paste-in snippet that asks before making a correction permanent, saves approved outputs to `references/examples/`, and requires a version bump.
- **`references/interview.md` rule 12** — 3–5 distinct numbered options with the recommendation as option 1 at every design choice; plain question + recommendation for facts only the user can answer.
- **12 new evals** covering the scope gate, the upgrade pass (edit and review-only), the invocation gate, 3–5 options, the self-improvement stamp, the functional eval, the connector ladder, version/changelog sync, changelog migration, and ai-file-manager on review-only sessions. 15 → 27 tests.

### Changed
- **SKILL.md cut 178 → 104 lines** and the frontmatter description cut ~1,050 → ~440 characters. Rules moved out of the description into the body (a rule in the description is paid for on every request and read on almost none).
- **Duplicated blocks removed from SKILL.md**, each now living in exactly one place: the Troubleshooting section → `references/edit-skill.md` (writable paths) and `references/packaging.md` (`present_files`, `.DS_Store`, temp files); the Packaging Quick Reference table → `references/packaging.md`; the slash-command registration procedure → `references/claude-code-skill.md` CC-6; the platform comparison table → `references/new-skill.md` Step 0; the `Tests Needed` list → `tests/evals.json` as real tests. SKILL.md keeps a "Known Environment Issues" pointer table instead.
- **`references/skill-quality.md`** — the old §4 quality gate is now §7, with six new gate items (invocation mode, steps-are-instructions, progressive disclosure, connectors, human checkpoints + options, self-improvement rule, prune + functional eval passed). §1 no longer holds up the old `AUTO-TRIGGER …` description as the model.
- **`references/claude-code-skill.md`** — CC-5 runs the Step 0D scope gate and the pre-done test/eval/prune sequence; CC-6 gained the rename procedure (write new command file, delete old, grep `~/.claude/commands/` and `~/.claude/scheduled-tasks/` for the old path).
- **`skill-builder-protocol` itself stays AI-invocable** — a deliberate, documented exception to the new §4 default, because its job is catching skill work in sessions where the user didn't type the command.

### Why
Reviewed against an external skill-creator skill and a set of best-practice prompts. The protocol was strong on process (phases, changelog, packaging, platform gate) and silent on artifact economics: nothing sized a skill, nothing shrank one, nothing decided invocation mode, nothing kept connectors out of context, and nothing stamped self-improvement into the skills it produced. It also violated its own leanness rule and contradicted itself on subagents. The upgrade pass is the load-bearing addition — without it these standards would only ever apply to brand-new skills, and every existing skill would stay at whatever standard existed the day it was built.

---

## [v1.15.0] — 2026-07-31 at 4:29 PM EST

### Added
- **New required gate: ask which category folder a new skill goes in.** The `Skills` base folder is now split into `generic-skills/`, `personal-skills/`, `work-skills/` (grouped by discipline). Skills live one level down, never at the base root.
  - `references/claude-code-skill.md` — new **Step CC-1b** between resolving the base folder and naming the slug: list the category folders that exist, recommend one, and wait for the user's answer. CC-3 now builds at `$BASE/$CATEGORY/$SLUG`, and CC-6 registers the slash command at `<base>/<category>/<slug>/skill/`.
  - `references/new-skill.md` — new **Step 0-folder** right after the Cowork-vs-Claude-Code gate, so the ask happens on both build paths.

### Why
The reorg means there is no single correct place to put a new skill anymore, and guessing wrong costs a folder move plus a broken slash command and any scheduled routine that hard-codes the path.

---

## [v1.14.0] — 2026-07-28 at 10:07 AM EST

### Changed
- **`skill-builder-protocol` itself standardized onto the shared project template** — moved to the `CLAUDE.md` / `MEMORY.md` / `skill/` / `outputs/` / `random/` layout used by every other Claude Code skill folder.
- **`assets/claude-code-template/CLAUDE.md` (the bundled scaffold this skill hands out for new Claude Code skills) replaced with the current condensed `0-template/CLAUDE.md`** — the old bundled copy was the pre-condensation bloated version (full Preferences/Rules/Working-style/Things-to-avoid/Self-Improvement-Loop sections duplicating what now lives in the global and parent `CLAUDE.md` files). Placeholders (`{Skill Name}`, `{skill-name}`, `{skill purpose}`) and the `### Preamble to drop in...` block were kept intact — new skills still need that preamble since they have no `CHANGELOG.md` yet.
- Confirmed `assets/claude-code-template/MEMORY.md` and `gitignore.txt` already matched `0-template/MEMORY.md` and `0-template/.gitignore` byte-for-byte — no changes needed there.
- Checked `references/*.md` for any instruction describing the old bloated CLAUDE.md section-by-section — found none; the reference files already treat the bundled template as a black box (CC-3/CC-4 in `claude-code-skill.md` just copies + fills placeholders), so no reference updates were required.

### Why
Part of a broader pass standardizing every Claude Code skill folder (including this one) onto the condensed template. Since this skill is also the one that scaffolds new skills, its bundled template copy needed to be brought current so future skills stamp out with the lean CLAUDE.md, not the retired bloated version.

---

## [v1.13.0] — 2026-07-22 at 2:09 PM EST

### Added
- **Platform gate for new skills — Cowork-installed vs Claude Code.** `references/new-skill.md` now opens with **Step 0**: before any build work, ask whether the user wants (1) a Claude Cowork installed skill (regular flow, packaged as a `.skill`) or (2) a Claude Code skill (plain files under `Skills/`, not installed, edited directly). SKILL.md gained a matching "⚙️ FIRST when building a NEW skill: pick the platform" section with a comparison table.
- **New `references/claude-code-skill.md`** — the self-contained Claude Code branch (CC-1…CC-6): resolve the `Skills` base dir (Dropbox path → `~/Documents` fallback), lowercase-dashed slug, stamp the project folder from the skill's **bundled** template, customize `CLAUDE.md`/`MEMORY.md` placeholders, build the skill inside the inner `skill/` folder, and register the `/<slug>` command pointing at `skill/`. No `.skill` packaging on this path.
- **Bundled, self-packaged template — `assets/claude-code-template/`** (`CLAUDE.md`, `MEMORY.md`, `gitignore.txt`). The Claude Code branch copies from here, so it works for any user who does NOT have the source `0-template` folder on their machine. Stored `.gitignore` as `gitignore.txt` so it survives packaging and lands correctly at copy time.
- **Three `platform-gate` evals** (`platform-001/002/003`): gate is asked before building; Claude Code choice stamps the folder from bundled assets + builds inside `skill/` + registers the command + produces no `.skill`; Cowork choice still runs the normal packaged flow.

### Changed
- **SKILL.md** — added the Claude Code branch row to Reference File Routing; the "Register a slash command" section now notes CC-branch skills point the command at the inner `<slug>/skill/` folder; added two `Tests Needed` lines for the platform gate.

### Fixed
- **`tests/evals.json` `phase-001`** — replaced "waits for David's input" with "waits for the user's input" (the skill's own rule bans personal names in skill files).

### Why
- The user wanted a second, lighter-weight way to create skills for Claude Code (plain files, no packaging, easy to edit) alongside the existing Cowork `.skill` flow, and wanted the whole thing self-packaged so teammates who don't have the local template folder can still use it. The generic template also had Google-Ads-specific leftovers (customer ID, a live Slack webhook, GAds verification steps) that didn't belong in a general-purpose template; those were genericized at the source (`0-template`) and in the bundled copy.

---

## [v1.12.0] — 2026-07-22 at 1:37 PM EST

### Added
- **New always-on SKILL.md section: "Register a slash command for every new skill" (Claude Code).** Whenever a new skill is created (or renamed), the protocol now writes `~/.claude/commands/<slug>.md` pointing at the skill folder, so the user immediately gets a `/<slug>` command with no app restart and no manual step. Silently skips when `~/.claude/commands/` doesn't exist (e.g. Cowork-only machines).

### Why
- On macOS, a shell/`launchd` auto-sync watcher (the "obvious" way to turn skill folders into slash commands) is blocked by TCC from *reading* skills stored in a CloudStorage/Dropbox folder — it silently finds nothing. Verified 2026-07-22: `find`/globs on a Dropbox `Skills/` path return "Operation not permitted," while the `Write`/`Read` tools are unaffected. Baking command-file creation into the skill-build workflow (via the `Write` tool) is the reliable fix — it runs at creation time with tools that aren't TCC-blocked, rather than depending on a background process that is.

---

## [v1.11.0] — 2026-06-16 at 11:28 AM EST

### Added
- **New `references/skill-quality.md` — "What Makes a Good SKILL.md (Artifact Quality)".** The skill was heavy on process discipline and Cowork plumbing but thin on what makes the *produced* skill good — it delegated all structural conventions to `skill-creator` (a black box not visible in these files). This new reference, adapted from the strongest parts of Matt Pocock's `write-a-skill`, teaches: (1) **the description is the trigger surface** — capability-first sentence + explicit `Use when [triggers]` clause, third person, ≤1024 chars, with a good-vs-bad example; (2) a **script-vs-inline decision rubric** (deterministic / repeated-generation / explicit-error-handling); (3) **progressive disclosure** stated as a named rule — lean SKILL.md, references one level deep, when to split; (4) a **finished-artifact quality gate** distinct from the process sync checklist.
- **`tests/evals.json` — `quality-001`** asserting a produced skill's description follows the capability-first + `Use when [triggers]` format.

### Changed
- **`SKILL.md` — added a Reference File Routing row** pointing to `skill-quality.md` (writing the description / scripts-vs-inline / splitting files / final quality gate).
- **`references/new-skill.md` Phase 2 — reconciled the SKILL.md length guidance.** Resolved a real contradiction: the old line said "under 500 lines" while artifact-quality thinking says lean. New single stance: *aim ~100–200 lines; 500 is a hard ceiling; push detail to reference files.* Added a pointer to load `skill-quality.md` before finalizing.
- **`references/edit-skill.md` Sync Checklist — added a description self-check** against `skill-quality.md` §1 whenever the frontmatter description is touched.

### Why
Analysis of `write-a-skill` surfaced that our protocol never taught *how to write a triggering description*, *when to write a script*, or stated the progressive-disclosure depth cap — all output-quality fundamentals. It also carried a live 100-vs-500 line contradiction. This release folds in those teachings as one on-demand reference without bloating the router.

---

## [v1.10.1] — 2026-05-06 at 3:45 PM EST

### Changed
- **`references/packaging.md` — surface ONE `computer://` link, not two.** v1.10.0 told Claude to drop both an "outputs primary" and "workspace backup" link in the chat reply. A real user reading the chat asked "how come you are presenting 2 skills to save?" — the dual-link pattern reads as two separate skills, not one + backup. New rule: save the workspace backup silently on disk, but only surface the outputs link in chat. Surface the backup link only if the user reports the primary is broken.
- **Updated SKILL.md version line.**

### Why
Test of the v1.10.0 doc against an actual user revealed the dual-link UX was confusing. The point of `computer://`-first was to be reliable AND clear; two links was reliable but not clear. One link is both.

---

## [v1.10.0] — 2026-05-06 at 3:30 PM EST

### Changed
- **`references/packaging.md` — flipped default to `computer://`-first.** v1.9.0 told Claude to try `present_files` twice before falling back. Verified empirically across 3 sessions: `present_files` ALWAYS fails on `.skill` files in this user's environment, regardless of path or perms. Trying it first wastes 2 tool calls every session. New default: copy `.skill` to BOTH workspace root AND outputs folder, chmod 644 both, drop two `computer://` links in the chat reply, tell the user to click → Finder → double-click. Use `present_files` only if explicitly requested by the user. Section retitled "Presenting the .skill File — Default to `computer://`".
- **`SKILL.md` — replaced the "present_files keeps rejecting" troubleshooting entry** with a more accurate "always fails in this environment" entry that points at the new default flow.

### Added
- **`references/packaging.md` — `.DS_Store` handling.** macOS auto-creates these in every folder Finder views, including staged skill folders. Pre-packaging cleanup must (a) include `.DS_Store` in the deletion target list, (b) handle `PermissionError` via `allow_cowork_file_delete` + retry, (c) explicitly skip `.DS_Store` in the zipfile loop as belt-and-suspenders.
- **`SKILL.md` — `.DS_Store` PermissionError troubleshooting entry.**

### Why
v1.9.0's `present_files` ladder assumed retries might work. Two consecutive sessions proved they don't. The new default trades aspiration for reliability — `computer://` works 100% of the time, so it should be the documented happy path. `.DS_Store` cleanup also bit me mid-packaging this session and wasn't covered in any prior version.

---

## [v1.9.0] — 2026-05-06 at 2:30 PM EST

### Added
- **`references/edit-skill.md` — "Path Reality Check" section at the top.** Documents that `request_cowork_directory` fails on `~/Library/Application Support/...` (protected) and the plugin cache `/var/folders/...` (sandbox), and that `mnt/.claude/skills/` is read-only. Adds a 4-row table of every possible skill location with writability status, and a "30-second path resolution flow" that resolves the writable workspace folder in 6 bash steps (ls mounts → mkdir → cp -r → chmod -R u+w → edit).
- **`references/edit-skill.md` — "File Permissions Gotcha" section.** Mandates `chmod -R u+w` immediately after every `cp -r` from `mnt/.claude/skills/`, since copies inherit the read-only mode and the first Edit will otherwise fail. Also documents the recovery if `cp -r` itself fails on a subfolder ("Permission denied" on existing read-only destination).
- **`references/packaging.md` — "Use the Fallback Ladder" section** replacing the old "Presenting the .skill File" section. Documents the 3-attempt retry cap (workspace root → outputs folder → `computer://` link), why each attempt fails, the requirement to `chmod 644` before presenting, and a hard rule that retries are capped at 2 before falling back to `computer://`.
- **`SKILL.md` — Two new top-level troubleshooting entries.** "Editing a live skill: which path is actually writable?" and "`present_files` keeps rejecting the .skill file." Both include hard rules and link back to the reference files for the full procedure.

### Why
Every skill edit session was burning 5–10 tool calls rediscovering the same path issues: protected `request_cowork_directory` paths, read-only mounts, copy-then-chmod ordering, and `present_files` rejecting nested paths. These fixes encode the working flow so the next session starts with the right path on the first attempt.

---

## [v1.8.0] — 2026-04-19 at 11:46 AM EST

### Added
- **Absorbed the `process-interviewer` skill into this one** so skill building no longer requires calling two skills. Added `references/interview.md` with the full interview script (4-step structure: Big Picture → Process Deep-Dive → Edge Cases → Confirmation), interview rules (one question at a time, always recommend an answer, don't accept vague answers), and a handoff to the brainstorm phase.
- Added a new routing table row in SKILL.md for `references/interview.md` so Claude knows when to load it.

### Changed
- **Renamed Phase 1 to Phase 1a (Interview) + Phase 1b (Brainstorm)** in `references/new-skill.md` and the 6-phase quick reference in SKILL.md. Phase 1a runs BEFORE brainstorming — it extracts a confirmed GOAL/INPUT/PROCESS/OUTPUT/EDGE CASES summary, which Phase 1b then refines. Prevents open-ended brainstorming on fuzzy requirements.

---

## [v1.7.0] — 2026-04-17 at 1:31 PM EST

### Changed
- **Updated ai-file-manager instructions** across SKILL.md, `references/edit-skill.md`, and `references/new-skill.md` — replaced "read this file" with a 3-step fallback sequence: (1) invoke the `/ai-file-manager` skill in Claude (preferred), (2) if unavailable, read the file directly at the known session path, (3) if still not found, tell the user and keep going without getting stuck. Makes the skill usable for shared teammates who may not have the skill installed at the same path.

---

## [v1.6.0] — 2026-04-15

- **Added Troubleshooting entry for stale temp files** — explains root cause (bash zip fails mid-write on mounted paths, leaves random-named temp files), fix (Python `zipfile` + pre-packaging scan), and delete approach (`os.remove()` → `allow_cowork_file_delete` on `PermissionError` → retry; never ask user to delete manually).
- **Added Packaging Quick Reference table** at end of SKILL.md — maps each operation (text files, binary assets, zip packaging, temp file deletion) to its correct tool, with pointer to `references/packaging.md` for full instructions.
- **Updated `references/packaging.md`** — added Pre-packaging section with Python snippet to detect and delete stale temp files before every zip run; updated "never use bash zip" note with correct temp file name example.

---

## [v1.5.1] — 2026-04-13 at 12:00 AM EST

### Added
- Added mandatory repackaging step to the sync checklist in `references/edit-skill.md` — every edit session must end with repackaging the `.skill` file and presenting it to the user, so the Claude desktop app stays in sync with the files on disk
- Added explanatory note in `edit-skill.md` clarifying *why* this is required: the desktop app reads from the installed `.skill` package, not raw files, so skipping repackaging leaves the installed skill out of date
- Updated routing table in `SKILL.md` to flag `references/packaging.md` as **required at the end of every edit session**

---

## [v1.5.0] — 2026-04-12 at 11:47 PM EST

### Changed
- Restructured SKILL.md from a 481-line monolithic document into an ~85-line routing document that directs Claude to load only the reference file needed for the current task
- Created `references/new-skill.md` — Steps 0A (ai-file-manager), 0B (versioning), 0C (model rec), Phase 0 (permissions), Phase 1 (brainstorm), Phase 2 (build rules) — loaded only when creating a skill from scratch
- Created `references/edit-skill.md` — Step 0A (ai-file-manager), sync checklist, version bump rules, brainstorm trigger for large edits — loaded only when editing an existing skill
- Created `references/changelog.md` — full changelog format, versioning rules, timestamp command, migration instructions — loaded only when writing or updating a changelog
- Created `references/packaging.md` — file type rules table, Python zipfile pattern, validation checks, present_files flow — loaded only when packaging a .skill file
- Created `references/phases.md` — Phase 3 (capture learnings), Phase 4 (tests), Phase 6 (build summary), default priorities — loaded at end of a build
- Added mandatory `ai-file-manager` read instruction to SKILL.md routing section — triggers on every use regardless of task type
- Added `superpowers:brainstorming` trigger note for large edits or significant restructuring

---

## [v1.4.0] — 2026-04-12 at 11:36 PM EST

### Added
- Added `.skill` Packaging Validation section with a Python snippet that runs 3 checks before `present_files`: (1) SKILL.md at root level, (2) exactly one SKILL.md, (3) no stale `.skill` files included
- Documented the three exact installer errors these checks prevent, with root cause explanation for each
- Added "Presenting the .skill File — Always From Session Working Directory" section explaining why `mnt/skills/` paths always fail with `[INVALID_PATH]` and the correct pattern: stage in `/tmp`, copy to `/sessions/<current-session>/`, then `present_files` from session dir

---

## [v1.3.0] — 2026-04-12 at 10:48 PM EST

### Changed
- Rewrote Cowork environment section with complete, correct file-writing rules covering all three cases: text files (Write/Edit tools), binary assets (Python shutil.copy2), and .skill packaging (Python zipfile staged in /tmp)
- Added reference table mapping file type to correct write method — eliminates ambiguity about when to use each approach
- Replaced old bash-based packaging snippet with working Python zipfile pattern
- Added explicit note that the installer rejects .skill files where SKILL.md is not at the zip root, with the exact error message ("Zip must contain a SKILL.md file")
- Added guidance that all folder creation (assets/, references/, etc.) should use Python os.makedirs to ensure they actually persist to the Mac

---

## [v1.2.9] — 2026-04-12 at 10:47 PM EST

### Added
- Binary file copy rule: the Write tool is text-only and bash cannot reach Mac paths — use Python `shutil.copy2` via the mounted path to copy PNGs and other binary assets into skill folders. Added to Cowork environment section alongside the packaging rule.

---

## [v1.2.8] — 2026-04-12 at 10:46 PM EST

### Added
- Manual packaging rule in Cowork environment section: always stage zip in `/tmp` first, then copy to skill folder — zipping directly into a mounted skills folder fails mid-write on network mounts (leaves stale temp files). Also documents that SKILL.md must be at the zip root level, not nested in a subfolder, or the installer will reject it.

---

## [v1.2.7] — 2026-04-12 at 10:23 PM EST

### Changed
- Removed all personal name references ("David") throughout SKILL.md — replaced with "the user" or "the user's" to make this a fully shared, generic company skill
- Updated YAML frontmatter description to remove personal name and add explicit rule: never include personal names in skill files, use "the user" instead
- Updated title line from "David's personal 6-phase protocol" to "A shared 6-phase protocol"

---

## [v1.2.6] — 2026-04-12 at 9:59 PM EST

### Fixed
- Added rule to always run `TZ='America/New_York' date '+%I:%M %p'` before writing any timestamp — never guess or estimate the time

---

## [v1.2.5] — 2026-04-12 at 9:58 PM EST

### Changed
- CHANGELOG.md format updated from table to prose style (matching ai-file-manager) — easier to read, with `## [vX.X.X]` headers, `### Added/Fixed/Changed` sections, and date format `YYYY-MM-DD at H:MM PM EST`

---

## [v1.2.4] — 2026-04-12 at 9:55 PM EST

### Fixed
- **Corrected wrong VM path guidance**: `mnt/skills/` is sandbox-only and does NOT persist to David's Mac. Correct approach is `request_cowork_directory` on the specific skill folder, which mounts at `mnt/<skill-name>/` with real write access that saves directly to David's Mac. Updated Step 0A path note accordingly.

---

## [v1.2.3] — 2026-04-12

### Fixed
- Fixed hardcoded session name in Step 0A — now uses dynamic `ls /sessions/*/mnt/skills/` pattern
- Added VM path note (mnt/skills/ = writable, mnt/.claude/skills/ = read-only, same dir)
- Updated migration scan to remove Desktop/Downloads, add Dropbox Skills old path

---

## [v1.2.2] — 2026-04-12

### Added
- Phase 2 constraint: prefer `Edit` over `Write` for file changes; only use `Write` when replacing the majority of a file

---

## [v1.2.1] — 2026-04-12

### Fixed
- Replaced "Dropbox Skills folder" reference with "Claude skills folder" to reflect new canonical skills path

---

## [v1.2.0] — 2026-04-10

### Changed
- Moved changelog out of SKILL.md into separate CHANGELOG.md; SKILL.md now shows version number only
- Step 0B updated to enforce new format and migrate embedded changelogs in existing skills

---

## [v1.1.1] — 2026-04-07

### Fixed
- Strengthened migration scan — must explicitly check `Application Support/Claude/local-agent-mode-sessions/` for stale copies and prompt David to delete them

---

## [v1.1.0] — 2026-04-07

### Added
- Mandatory ai-file-manager review step at top of workflow
- Mandatory version number + changelog requirement for all skills

---

## [v1.0.0] — 2024-01-01

### Added
- Initial release
