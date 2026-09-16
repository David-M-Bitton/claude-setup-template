# Reference: New Skill — From Scratch

Load this file when **creating a brand new skill** (not editing an existing one).

---

## Step 0 — FIRST: ask which kind of skill (Cowork-installed vs Claude Code)

Before anything else — before the save-path check, model recommendation, or the interview — ask the user which kind of skill they want. These build to different places and have different maintenance.

> **Which kind of skill do you want?**
> 1. **Claude Cowork installed skill** — the regular flow. Built, packaged as a `.skill` file, and installed into the Claude desktop app. *(Recommended if you want it available across the app and shareable as a `.skill`.)*
> 2. **Claude Code skill (not installed, easier to edit)** — a plain folder of files under your `Skills` directory. Nothing is zipped or installed; you edit the files directly whenever you want to change it. Gets a `/<slug>` slash command.

How the two differ — they run the same interview, brainstorm, and scope gate; only the destination and shipping differ:

| | Cowork-installed | Claude Code |
|---|---|---|
| Where it's built | staged skill folder → `.skill` zip | `Skills/<category>/<slug>/` on disk |
| Ships as | a `.skill` file the user imports | plain files, read live — nothing to package |
| Load the branch | this file + `references/packaging.md` | `references/claude-code-skill.md` |

- **If they choose Claude Code (option 2):** load `references/claude-code-skill.md` and follow it. That path replaces Steps 0A→Phase 2 below with its own CC-1…CC-6 steps (it still runs the Phase 1a interview and Phase 1b brainstorm). Do **not** package a `.skill` for this path.
- **If they choose Cowork-installed (option 1):** continue with Step 0A below as normal, and package a `.skill` at the end (`references/packaging.md`).

If the user doesn't state a preference, recommend option 1 (Cowork-installed) unless the session is clearly a Claude Code session, in which case recommend option 2.

### Step 0-folder — confirm where the skill folder goes

The source files land in their own named subfolder directly inside the `Skills` base, never as a loose `SKILL.md` at its root. Full details for the Claude Code path: `references/claude-code-skill.md` Step CC-1.

---

## Step 0A — Confirm Save Paths FIRST

**One home for this rule: `SKILL.md` → "Always: Confirm Save Paths First".** Follow it there — where skills live, the migration scan, and the Cowork/Claude Code carve-out. Don't re-derive it from this file.

Do it before anything else: before model recommendations, brainstorming, or writing content. Do not proceed until the migration scan is complete.

---

## Step 0B — Version Numbers and Changelogs

Every new skill MUST have:

1. A version line in SKILL.md immediately after YAML frontmatter (**Claude Code path: there is no frontmatter — the version line sits under the `#` title heading. See `references/claude-code-skill.md` RULE CC-0**):
   ```markdown
   **Version: v1.0.0** — Full history in [CHANGELOG.md](./CHANGELOG.md).
   ```

2. A `CHANGELOG.md` file in the skill folder:
   ```markdown
   # Changelog — [skill-name]

   All notable changes to this skill are documented here.
   Format follows semantic versioning: MAJOR.MINOR.PATCH
   Date format: `YYYY-MM-DD at H:MM PM EST` (e.g. `2026-04-12 at 9:55 PM EST`)
   > ⚠️ **Always run `TZ='America/New_York' date '+%I:%M %p'` before writing any timestamp.** Never guess.

   ---

   ## [v1.0.0] — YYYY-MM-DD at H:MM PM EST

   ### Added
   - Initial release — [brief description of what the skill does]
   ```

---

## Step 0C — Model Recommendation

Recommend a Claude model before starting. Present this to the user:

> 📌 **Recommended model: [Model Name]**
> **Why:** [1–3 sentences on complexity, reasoning requirements, cost sensitivity]
> **Alternative:** [Close second and when you'd switch]

| Model | Use When |
|-------|----------|
| **Claude Opus** | Highly complex — multi-step reasoning, intricate logic, chaining many tools |
| **Claude Sonnet** | Moderately complex — default for most skill builds |
| **Claude Haiku** | Simple, well-defined — fast, low-cost, single-step tasks |

---

## Step 0D — Scope Gate (REQUIRED — before the interview)

Decide the skill's single job before extracting its process. A skill that does two jobs is unreliable at both.

**1. Is a skill worth building?** Build one when the task recurs — a repetitive task, a correction the user keeps giving, context they keep re-pasting, or a process they want to hand off. A genuine one-off doesn't need a skill; if it won't repeat, say so and stop.

**2. Name the single job in one sentence,** as "[verb] [object]": "draft a win-back email for one churned customer", "convert one Notion export to clean Markdown". If you can't state it in one sentence, the scope is too wide. Narrow until you can.

**3. Apply the "and" test.** If the one-sentence job needs "and" to be accurate, it is more than one job — propose splitting it into a chain of small skills, each built and tested on its own. Internal steps don't count: one job with eight steps is still one skill. Multiple *jobs* is what you split.

**4. Right-size it.** Don't scope an entire end-to-end process into one skill. Name the smallest slice that produces value on its own and confirm you're building only that. If the split is genuinely unclear, default to one skill for the one job now, and tell the user: build it, use it, split it later if it drifts or gets unreliable.

**Output of Step 0D — confirm both with the user before starting the interview:**

- The one-sentence job statement.
- The one-skill-or-several decision, with reasoning, plus the list of skills if splitting.

**Ship small, then iterate.** The first version is decent, not final. Expect 2–5 improvement loops driven by real use. Don't try to produce a complete, polished skill in one pass.

---

## Phase 0 — Permissions Upfront

**Folder access check — remind the user:**

> ⚠️ **Folder permissions check:** Make sure you've selected all necessary folders in Cowork:
> - **The knowledge base** (`~/Documents/Claude/Context/`) — for reference docs, ideal customer, brand guidelines
> - **The folder for this specific task** — input files or working documents
> - **The Skills folder** (`/.claude/skills/`) — so Claude can read and write SKILL.md directly

Wait for confirmation before continuing.

**Permissions ask** — identify every permission needed and ask in a single message:
- Unlimited browser access
- Unlimited read/write to files
- Permission to install packages / run terminal commands
- Any other action requiring mid-task confirmation

Wait for the user's go-ahead before Phase 1.

---

## Phase 1a — Interview First (Extract the Plan)

**Before brainstorming or writing any SKILL.md content, run the process interview.** Load `references/interview.md` and follow it end-to-end.

The interview extracts a complete, unambiguous plan from the user's head:
- GOAL / INPUT / PROCESS / OUTPUT / EDGE CASES
- One question at a time, always with a recommended answer
- Doesn't advance until each step is specific enough to implement
- Ends with a summary the user confirms is accurate

**Do not skip this step — even if the user seems confident.** The interview reveals gaps they didn't know they had. It prevents rewrites later.

Output of Phase 1a: a confirmed GOAL/INPUT/PROCESS/OUTPUT/EDGE CASES summary that Phase 1b will refine and Phase 2 will implement.

---

## Phase 1b — Brainstorm Refinements

Now that the plan is captured, run a structured brainstorm against it:

1. What are 3–5 ways to make this skill smarter, more reliable, or easier to maintain?
2. What edge cases or failure modes should we anticipate?
3. Are there simpler approaches that avoid unnecessary complexity?
4. What would make this skill break in real usage?
5. What would make it a joy to use vs. a pain?

Conduct the brainstorm inline, using the interview rules from `references/interview.md` — one question at a time, each carrying your recommended answer, 3–5 concrete numbered options at every design choice. Don't hand this to a plugin or a subagent; the user must be in the room for it.

**Do not proceed to Phase 2 until the user has reviewed and aligned on the approach.**

Output: A short agreed-upon design summary (3–5 bullet points) that Phase 2 will implement.

---

## Phase 2 — Build Durably

Implement the skill following these constraints:

- **Clear**: Unambiguous to a future Claude with no session context
- **Maintainable**: No clever tricks that are hard to modify
- **Reusable**: Write for the general case
- **No fragile shortcuts**: If robust handling is needed, do it robustly
- **Subagents only where `references/connectors.md` allows them** — connector calls, live research, evals, bulk mechanical reading. Never for the skill's own core process
- **Prefer `Edit` over `Write`**: Use targeted Edit (find-and-replace) when modifying existing files. Only use Write when replacing most of a file's content

Structural conventions (from `skill-creator`):
- YAML frontmatter with `name` and `description` — **packaged / Cowork `.skill` path ONLY.** On the Claude Code path, `SKILL.md` gets **no frontmatter at all** (`references/claude-code-skill.md` RULE CC-0), so the skill never auto-triggers and is reached only via `/<slug>`.
- Version line immediately after frontmatter (Claude Code path: under the `#` title heading)
- **Keep SKILL.md lean — aim ~100–200 lines; 500 is a hard ceiling.** Push detail into reference files and load them on demand. See `references/skill-quality.md` for the progressive-disclosure rule (references one level deep) and when to split.
- Store scripts in `scripts/`, reference docs in `references/`, templates in `assets/`
- Never include personal names — use "the user" throughout

**While building, load `references/skill-quality.md`** and apply it: the description rubric (§1), script vs inline (§2), progressive disclosure (§3), the invocation-mode gate — `disable-model-invocation: true` by default (§4), human checkpoints plus 3–5 options at every design choice (§5), and the embedded self-improvement rule (§6). If the skill touches a connector, MCP, or live research, load `references/connectors.md` first and decide whether you actually need it.

**Before calling the skill done, in this order:**

1. Phase 4 tests — `tests/evals.json` (`references/phases.md`).
2. Phase 4b functional eval — fresh session, 3 subagents (`references/phases.md`).
3. Phase 4c prune pass — deletion test on every paragraph (`references/prune.md`).
4. The §7 artifact quality gate in `references/skill-quality.md`.
