# MCP, CLI & API Connectors — How-To

Read before any MCP, CLI, API, or Claude connector work.

## Every connector gets its own memory file — create it on first use

🔴 **The first time you use a tool that has no `Memory/<Tool>/MEMORY.md`, create it in that same session.** Don't ask first, don't leave it for later. A connector you had to debug once and didn't write down costs the same debugging round every time.

<!--os:mac-->
- **Before using a tool, read its file.** Can't find it? `ls ~/Documents/Claude/Memory/` before concluding it doesn't exist — the folder may be named differently than the tool.
<!--/os:mac-->
<!--os:win-->
- **Before using a tool, read its file.** Can't find it? `dir "%USERPROFILE%\Documents\Claude\Memory"` before concluding it doesn't exist — the folder may be named differently than the tool.
<!--/os:win-->
- **The file holds four things, briefly:** what the tool is for, how it authenticates, the exact command or call that worked, and the gotchas.
- **Fixed an error, or learned something reusable? Append the rule to THAT tool's file** — never to this one. Rules only, do-this / don't-do-that. No stories, no dates, no "as of" notes.
- **Tighten or replace an existing rule instead of appending a near-duplicate.** A file that only grows stops being read.
- **Add a one-line router row** to the memory-router table in `~/.claude/CLAUDE.md` so the next session finds it.
- **Tell the user what you saved.**

🔴 **Secrets — API keys, tokens, passwords — live only in the local memory file or the machine's own config.** Never paste them into a shared doc, a note-taking app, a ticket, a commit, or any surface that syncs to other people.

## Checking whether a connector is actually available

**Run `ToolSearch` with the service's keyword.** That reflects the real callable-tool list. A registry or "list connectors" call can under-report — an empty result is NOT proof the connector isn't connected.

If `ToolSearch` also finds nothing, don't tell the user to reconnect yet. Ask them to confirm it in Settings → Connectors, then retry: tool exposure can lag the start of a session, and newly added MCP servers only load after a restart.

🔴 **The filesystem is not the source of truth for anything system-managed.** A leftover folder does not mean a connector is registered, and a missing folder does not mean it isn't. Ask the system: list the tools, query the connector, read the response.

## Wiring up a new MCP server

<!--os:mac-->
- 🔴 **Never use a bare command name in the config — always run `which -a <cmd>` first and use the absolute path.** A short name can collide with a system binary and the server then fails silently. (Real example: a tool shipping a CLI called `od`, while macOS already has `/usr/bin/od`.)
<!--/os:mac-->
<!--os:win-->
- 🔴 **Never use a bare command name in the config — always run `where <cmd>` first and use the absolute path.** A short name can collide with a built-in command or another program on `PATH`, and the server then fails silently. `where` lists every match in `PATH` order; the first one is what would actually run.
<!--/os:win-->
- **Don't create a global shim to fix a collision** — it shadows the system tool for every script on the machine. Use the absolute path instead.
<!--os:mac-->
- **A vendored GUI app usually hides its CLI inside the bundle** even when nothing is on `PATH`: `find /Applications/<App>.app -name '<cmd>*'` before concluding it isn't installed.
<!--/os:mac-->
<!--os:win-->
- **A GUI app usually ships its CLI inside its own install folder** even when nothing is on `PATH`: `dir /s /b "%ProgramFiles%\<App>\<cmd>*"` (also check `%LOCALAPPDATA%\Programs\`) before concluding it isn't installed.
<!--/os:win-->
- **Drop any hardcoded `--port` / `--url` flag if the server can auto-discover.** Those ports are often ephemeral and the config goes stale.
- **New MCP servers load only after a restart of the client.** Don't debug a "missing" tool before restarting once.
- **Per-machine config does not sync.** If the user works on more than one computer, write the exact `claude mcp add …` command into that tool's memory file so the second machine is one paste away.

## CLI gotchas worth checking first

- **Cached auth tokens outlive a re-login.** Several CLIs keep a token cache that a fresh `login` does not invalidate — new scopes show as granted while calls still return 403. Deleting the token cache file and re-running is the fix.
- **Some CLIs only accept file paths inside the current working directory.** Any absolute path outside it fails with "resolves to … outside the current directory." `cd` to the folder first, or write into the task's own folder and clean up after.
- **Read `<cmd> --help` before composing a command.** Published docs drift from the installed version, and arguments are often positional rather than flags.

## When no connector exists

For a desktop GUI app with no MCP server, check whether an agent-native CLI harness already exists before building a connector yourself. Install on demand; never vendor someone's whole repo into the knowledge base. This is a fallback for apps with no connector — it does not diagnose or fix a broken MCP.
