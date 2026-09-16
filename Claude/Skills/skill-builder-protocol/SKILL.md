---
name: skill-builder-protocol
description: Workflow protocol for building, editing, reviewing, or fixing a skill. Use when the user says "build a skill", "create a skill", "new skill", "update this skill", "fix this skill", "review this skill", "turn this into a skill", or when the session's goal is producing or improving a SKILL.md. Always pair with skill-creator. Enforces a phase sequence (scope, interview, brainstorm, build, test, prune, sync) plus an upgrade pass on every edit.
---

**Version: v1.23.0** — Full history in [CHANGELOG.md](./CHANGELOG.md).

---

## What This Skill Does

Governs **workflow discipline** for every skill build, edit, or fix. It overlays `skill-creator`, which owns structural conventions, eval mechanics, and packaging.

**This is a routing document. Load only the reference file the current step names — never all of them.**

Non-negotiable, every session: never skip the scope gate, the interview, the brainstorm, the prune pass, or tests. Never silently fix a failure — capture it. Never put personal names in skill files; write "the user".

---

## Always: Confirm Save Paths First

**Before anything else in the session, including a read-only review** — not just before a file touches disk — confirm where files go and run the migration scan. Both are stated here in full. **This is the one home for this rule**; `references/new-skill.md` Step 0A and `references/edit-skill.md` Step 0A point here — don't restate them there.

**Where skills live.** Every skill is its own named subfolder — kebab-case, matching the slug — directly inside `~/Documents/Claude/Skills/`. One folder per skill, never a loose `SKILL.md` at the root. Folder layout and required files: `references/claude-code-skill.md` Step CC-1.

**Migration scan** — check for stale copies loose at the `Skills/` root. **A stale copy is any loose `SKILL.md` or `.skill` file that is not inside a named skill subfolder**, or a second folder with the same skill slug. On the Cowork path also check `/sessions/*/mnt/` outside `mnt/skills/`, and `mnt/skills/` without a subfolder. If a stale copy is found, tell the user the exact path and let them delete it.

**Cowork path only.** Writable-path resolution (`request_cowork_directory`, `/sessions/*/mnt/` mounts, the chmod gotcha) is in `references/edit-skill.md` Step 0B; `.skill` packaging and `computer://` links are in `references/packaging.md`. On the Claude Code path skip both — the folder on the user's Mac is directly writable.

**Scheduled tasks are out of scope for this skill.** If the session also wires up a routine that runs the skill, read `~/Documents/Claude/Memory/routines.md` first — it owns routine prompts, spec-file location, naming, and permissions blocks.

---

## Start Here — Which Task Is This?

| The user wants to… | Go to |
|---|---|
| Build a **new** skill | `references/new-skill.md` — Step 0 platform gate, Steps 0A–0D, Phase 0 permissions, Phases 1a/1b, Phase 2 |
| Build a new **Claude Code** skill (option 2 at the gate) | `references/claude-code-skill.md` — self-contained CC-1…CC-6 |
| **Edit, review, fix, or shrink** an existing skill | `references/edit-skill.md` — writable-path check, the **upgrade pass**, sync checklist, version rules. **Load it before reading any file in the target skill** — it names what to read and in what order |

A new skill starts with the platform gate: Cowork-installed (packaged `.skill`) vs Claude Code (plain folder, edited live, gets a `/<slug>` command). Both run the interview and brainstorm. Full comparison and both branches: `references/new-skill.md` Step 0.

---

## Reference File Routing — Load at the Step That Needs It

| Step or task | Load |
|---|---|
| Scope the skill — one job, split or not | `references/new-skill.md` Step 0D |
| Run the process interview (Phase 1a) | `references/interview.md` |
| Write the description, choose script vs inline, set invocation mode, add human-in-the-loop options, embed self-improvement, run the artifact quality gate | `references/skill-quality.md` |
| The skill touches a connector, MCP, or live research — or you're deciding on a subagent | `references/connectors.md` |
| Capture learnings, write tests, run the functional eval, deliver the build summary | `references/phases.md` |
| Cut the skill down before shipping | `references/prune.md` |
| Write or update a changelog | `references/changelog.md` |
| Package the `.skill` zip (Cowork path only) | `references/packaging.md` |
| Register or repair a `/<slug>` slash command | `references/claude-code-skill.md` Step CC-6 |
| **Write a Claude Code `SKILL.md` — NEVER give it YAML frontmatter** | `references/claude-code-skill.md` **RULE CC-0** |

For large edits or significant restructuring, run the interview in `references/interview.md` before writing anything — **after** the Upgrade Pass approval gate, never before it. The audit comes first; the interview shapes what you build with the answers, not whether you audit.

---

## The Phase Sequence

Work in order. Do not skip or batch phases.

| Phase | Name | Key action |
|---|---|---|
| 0 | Permissions | Confirm save paths + migration scan (above) → ask for all folder and tool access upfront |
| 0D | Scope | One-sentence "[verb] [object]" job. Apply the "and" test. Split into a chain if it's more than one job. **List the existing skills first and confirm this isn't one of them** |
| 1a | Interview | Extract GOAL/INPUT/PROCESS/OUTPUT/EDGE CASES — one question at a time, 3–5 options at every design choice |
| 1b | Brainstorm | Align on the approach before writing any content |
| 2 | Build | Implement durably — clear, maintainable, unambiguous to a future session |
| 3 | Capture | Write failures and non-obvious learnings into the skill |
| 4 | Test | Tests alongside features, in `tests/evals.json` |
| 4b | Functional eval | Fresh session, 3 subagents: right order, reference files loaded on demand, connector called correctly |
| 4c | Prune | Deletion test on every paragraph — `references/prune.md` |
| 5 | Keep updated | Version bump + changelog row after every change |
| 6 | Review | Build summary → optional optimization pass |

**Editing an existing skill runs the same standards** through the **upgrade pass** in `references/edit-skill.md` — eight checks: scope, invocation mode, description, size and progressive disclosure, steps-are-instructions, connectors, human-in-the-loop, self-improvement (8a) and duplication (8b). That file is the authoritative list; don't audit from this line. Prune and the functional eval come *after* the approval gate, not during the audit. An edit session is also a cleanup session — audit, report, get approval, then apply.

---

## Subagents

Allowed for connector and MCP calls, live research, the Phase 4b functional eval, and bulk mechanical reading — anything that returns a small, clean result. Not for the build itself, the interview, the brainstorm, or any step the user must approve. Details and the return-shape rule: `references/connectors.md`.

---

## Integration With skill-creator

`skill-creator`: structural conventions, eval mechanics, packaging, description optimization.
This skill: phase sequencing, scope and prune discipline, brainstorm enforcement, test-as-you-go, learning capture, sync.

When both are in context, this skill's phase sequence governs session structure.

---

## Known Environment Issues

Don't rediscover these — each is documented with its fix:

| Symptom | Where the fix lives |
|---|---|
| No writable path to a live skill (`request_cowork_directory` rejects it; `mnt/.claude/skills/` is read-only) | `references/edit-skill.md` → path reality check |
| `present_files` fails on every `.skill` file | `references/packaging.md` → present with `computer://` links instead |
| `os.remove()` PermissionError on `.DS_Store`, or stale temp files landing in the zip | `references/packaging.md` → pre-packaging cleanup |
| Shell or launchd can't read Dropbox-backed skill folders (macOS TCC) | `references/claude-code-skill.md` CC-6 → use the `Write` tool, never a shell script |

Never use bash for anything touching mounted Mac paths — use `Read`/`Write`/`Edit` and Python.
