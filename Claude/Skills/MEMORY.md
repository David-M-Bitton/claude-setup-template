# MEMORY.md — top-level index (cross-skill)

This is the first file to read each session (per this folder's `CLAUDE.md` → "Memory System"). It holds **cross-skill facts** and an **index** of the skills installed here. Skill-specific facts live in that skill's own folder; reusable how-tos and profile facts live in `~/Documents/Claude/Memory/`.

**Where new memory goes** (and **self-update proactively** — if you learn something during a session that would help future sessions, write it to the right file now, don't wait to be asked):
- **Cross-all-skills fact** → here.
- **Topic/domain fact or how-to** → that topic's file in `~/Documents/Claude/Memory/` (e.g. `personal.md`, `company.md`, `website-crawling.md`, or a per-connector file).
- **One-skill fact** → that skill's own `MEMORY.md`.
- **Behavior rule** ("always/never/before X do Y") → the relevant `CLAUDE.md`, not memory.

## Skills index

Skills that ship with this setup (each in its own subfolder). Add a line whenever you create a new skill.

- **`skill-builder-protocol`** — the 6-phase workflow for building or editing any skill (brainstorm → build → capture → test → update → review). Use it (with `skill-creator`) whenever you create or change a skill.
- **`process-interviewer`** — interviews the user until a fuzzy idea becomes a concrete, unambiguous plan. Use before building anything complex; it can hand off straight into `skill-builder-protocol`.
- **`the-humanizer`** — rewrites copy so it reads like a human, not AI. Use for any public-facing writing.
- **`0-template`** — the starter folder structure for a new skill project. Copy it; don't fill it in place.

## Cross-skill facts

- **Folder layout.** The knowledge base lives under `~/Documents/Claude/` with four folders:
  - `Context/` — durable documents about the user and their company (`Personal/`, `Company/`, optional topic hubs). Each subfolder has a decision-tree `CLAUDE.md`.
  - `Memory/` — all memory files in one folder, one per topic (profile facts + reusable how-tos + per-connector notes).
  - `Skills/` — the skills (this folder).
  - `Tasks/` — one named subfolder per scheduled task or ongoing working job.
  - All cross-references use **absolute paths** so future moves don't break them.
- _(Add other cross-skill facts here as they come up.)_
