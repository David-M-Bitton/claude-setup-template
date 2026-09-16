# Company Context — read only what the task needs

This folder holds documents about the company. **Don't load everything every session** — that wastes tokens. Use the decision tree below to open ONLY the file(s) a task actually needs.

Quick profile facts live in `~/Documents/Claude/Memory/company.md` — read that first for a one-screen summary. Come into this folder only when a task needs the full detail.

## Decision-tree matrix

> Keep this table current. **Whenever you add, rename, or remove a file in this folder, update a row here in the same session** — list the file, when to read it, and skip it otherwise. This table is how future sessions decide what to open.

| If the task is about… | Read | Otherwise |
|---|---|---|
| A quick "what does the company do / who do they sell to" answer | `~/Documents/Claude/Memory/company.md` | — |
| _(add rows as you add files — e.g. "brand voice / writing tone" → `brand-voice.md`)_ | `<file>` | skip |
| _(e.g. "ideal customer / target audience / positioning")_ | `<file>` | skip |
| _(e.g. "product details / pricing / features")_ | `<file>` | skip |
| _(e.g. "team / who's who / org chart")_ | `<file>` | skip |
| _(e.g. "strategy / goals / OKRs")_ | `<file>` | skip |

If no row matches the task, don't open anything here — answer from `Memory/company.md` or ask.
