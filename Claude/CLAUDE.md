# `~/Documents/Claude/` — Keep This Folder Clean

This is the home for your Claude knowledge base. It has exactly five working folders:

- `Context/` — durable context about you and your company.
- `Memory/` — all memory files (one file per topic, or one folder per tool/connector).
- `Skills/` — your skills.
- `Scheduled/` — one subfolder per scheduled routine. Its `CLAUDE.md` is the shared rulebook every routine follows.
- `Tasks/` — one subfolder per ongoing working job.

## ⚠️ Never auto-create files or folders here

**Do NOT create new files or folders directly in `~/Documents/Claude/` on your own initiative.** No scratch files, no outputs, no logs, no "temp" folders, no new top-level folders. Keep this directory clean.

When you need to write something, put it in the right place **inside an existing folder**:

| What you're saving | Where it goes |
|---|---|
| A memory fact / how-to note | a file inside `Memory/` |
| Notes about a specific MCP, CLI, API, or connector | `Memory/<Tool Name>/MEMORY.md` — create it the first time you use that tool |
| A scheduled routine's spec, outputs, or scratch | that routine's own subfolder inside `Scheduled/` (never a loose file in `Scheduled/` itself) |
| Context about me or my company | the matching folder inside `Context/` (`Personal/` or `Company/`) |
| Skill files / skill outputs | inside that skill's own subfolder under `Skills/` |
| Files for an ongoing working job | that job's own named subfolder inside `Tasks/` (create the subfolder; never loose files in `Tasks/` itself) |

## When the right place doesn't exist

If there's genuinely no correct existing folder for what you need to write, **stop and ask me** where it should go and whether a new folder is warranted — don't guess, and don't default to creating one at this root. Only create a new top-level folder here if I explicitly approve it.
