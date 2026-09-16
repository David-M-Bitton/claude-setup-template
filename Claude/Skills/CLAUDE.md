# Skills Folder — Claude Instructions

This is the top-level Skills directory. **Each skill lives in its own named subfolder.** Use `0-template/` as the starting point when creating a new skill.

## ⚠️ CRITICAL: Never create or edit files directly in this folder

Do NOT create, edit, or place any files — skill files, `SKILL.md` files, reference files, temporary files, output files, `.skill` packages, or anything else — directly inside this `Skills/` directory.

Every skill has its own named subfolder. All work must happen inside the correct subfolder.

## Correct behavior

If you are working on a skill, always locate or create its subfolder first:

```
Skills/
└── my-skill/               ← work here, not in the Skills root
    ├── skill/
    │   ├── SKILL.md
    │   ├── CHANGELOG.md
    │   ├── references/
    │   └── tests/
    │       └── evals.json
    ├── outputs/            ← outputs from running the skill
    ├── random/             ← scratch / drafts
    └── MEMORY.md           ← skill-specific facts
```

**Example:** If you have access to the whole Skills folder and are updating the `the-humanizer` skill, every read/write/edit goes to `the-humanizer/` (or its subfolders) — never to the Skills root.

## Creating or editing a skill

- **Always use the `skill-builder-protocol` skill** (it owns the 6-phase workflow: brainstorm → build → capture learnings → test → keep updated → review) together with `skill-creator`. Copy `0-template/` as the starting folder structure.
- Never create a loose `SKILL.md` or `.skill` file at the Skills root.
- **Reinstalling:** if a skill needs to be installed into Claude, repackage it as a `.skill` file. If it's a Claude Code skill (a plain folder, not an installed Claude skill), there's no need to repackage it — leave it as a folder.

---

## Memory System

There are three tiers of memory. **Read the relevant ones at session start** (don't announce what you found — just be informed):

1. **Top-level cross-skill** → `./MEMORY.md` (this folder). Facts useful to every skill. Read first, every session.
2. **Shared per-domain / how-to** → `~/Documents/Claude/Memory/*.md` — one file per topic (profile facts like `personal.md`/`company.md`, plus reusable how-tos like `task-delegation.md`, `website-crawling.md`, `self-improvement.md`, and one file per connector/MCP/CLI you set up). Read the matching file whenever a task touches that topic.
3. **One-skill** → that skill's own `MEMORY.md`. Read when working inside that skill's folder.

### ⭐ Always self-update memory (most important rule)

The moment you learn something a **future session** would want — a working command, a gotcha, a confirmed number, a definition, a fix — **write it to the right file immediately, on your own initiative. Do NOT wait to be asked.** This is how the whole workspace gets smarter; skipping it silently wastes every future session's time. Same routing whether you decided to save it or the user said "remember this" (then also confirm):

- Helps **every** skill → top-level `./MEMORY.md`
- Helps **one topic/domain** → that `~/Documents/Claude/Memory/<topic>.md` file
- Helps **one skill** → that skill's `MEMORY.md`
- It's a **behavior rule** ("always/never/before X do Y") → the relevant `CLAUDE.md`, not memory

Keep entries short and durable; update an existing line rather than duplicating. When genuinely unsure which file, pick the best fit and note it; only ask if it's truly ambiguous.

---

## Rules

- Ask clarifying questions before starting a complex task if the request is ambiguous.
- If you're not sure about something, say so. Don't guess.
- Read the active skill's `SKILL.md`, its `CLAUDE.md`, and relevant reference files at session start before starting work on it.
