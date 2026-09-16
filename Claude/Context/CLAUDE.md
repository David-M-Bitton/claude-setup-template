# Context — Claude Instructions

## What this folder is

`Context/` is your **durable knowledge base about yourself and your company**. It is **not a skill and not a scratch space**. Skills and sessions read from here (by absolute path) so every session shares the same facts.

It has two standard folders, plus optional topic hubs you add over time:

| Folder | Holds |
|---|---|
| `Personal/` | Documents, notes, and files about **you** — bio, preferences, projects, anything personal you want Claude to know. |
| `Company/` | Documents, notes, and files about **your company** — what it does, who it sells to, brand voice, strategy, team, tools. |
| `<Topic>/` (optional) | A hub per data domain you work in often (e.g. a tool, an account, a recurring report). Each hub holds the durable facts for that domain. |

Each folder has its own `CLAUDE.md` with a **decision-tree matrix** — read that first and open ONLY the file(s) a task needs, so you don't waste tokens loading everything every session. Keep the matrix updated as files are added.

## How this relates to Memory/

Two layers, different jobs:

- **`Context/` (this folder)** = the **full documents** — long files, exports, references you dump in.
- **`~/Documents/Claude/Memory/`** = the **short, durable facts**. `Memory/personal.md` and `Memory/company.md` are the quick-read profile summaries; other `Memory/*.md` files hold reusable how-tos (data fetching, task delegation, connector notes, etc.).

When a task needs a quick fact about you or the company, read the `Memory/` summary first; open the full `Context/` documents only when you need the detail.

## How to work here

- **✅ Self-update on your own initiative.** The moment you learn a durable fact a future session would want, save it to the right place now — a short fact to the matching `Memory/` file, a full document to the matching `Context/` folder. Update an existing line rather than duplicating.
- **⚠️ Ask first** before creating, renaming, moving, or deleting any folder here, and before editing bulk reference DATA files (CSV/JSON/exports). Those aren't casual edits.
- **❌ Never write loose files to this root.** Everything lives inside `Personal/`, `Company/`, or a named topic hub.
