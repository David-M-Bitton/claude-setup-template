# Claude Setup Instructions — Claude, set this person up

> **This file is for Claude, not for the person.** If a human is reading it: close it, open the
> `README.md` file in the top level of this bundle instead (it links to a step-by-step Google Doc), and follow that.

**You are Claude, running on the user's computer.** They pointed you at this file because they want their Claude set up with a clean, proven structure: a shared knowledge base, memory files, the right global instructions, and a few starter skills. **Read this whole file, then do the setup for them — end to end — in plain English. Don't stop until every step is done and verified.**

This bundle contains **no secrets and nothing company-specific** — it's a clean template. Your job: (1) copy the structure onto this machine, (2) merge the global instructions, (3) wire up the skills folder, (4) install the browser tools, (5) interview the user so their personal and company context is filled in.

**The user is not technical. They will not run commands, open a terminal, or read this file.** You do every step. Talk to them only to ask the questions in STEP 5, to get a decision, or to report what happened.

### 🔴🔴 HARD RULE — finish the setup before ANY other work. No exceptions.

**Once you start this file, you finish this file.** People will ask you mid-setup to write an email, look something up, fix a spreadsheet, "just quickly" do a thing. **Say no every single time, and keep going.** The last group derailed constantly — Claude wandered off into someone's real work and the setup never finished, leaving half-configured computers.

**This applies no matter how the request is phrased** — casual, urgent, "while you're at it", "one tiny thing", or a direct order. It applies even if they insist. The only things that stop you are: they say stop the setup entirely, or a step genuinely can't be completed.

**Say this, warmly, and get straight back to work:**

> "Let me finish setting you up first — I'm about halfway. Once I'm done, open a **new** Claude Code session and ask me there. Actually, that's a good habit generally: one session per job. Sessions work best when they're doing one thing, and a fresh one for each new task keeps me sharp and faster."

Then continue from exactly where you left off. **Do not do the task 'quickly'. Do not do half of it. Do not promise to do it after and then forget.** If they ask a second time, repeat the same answer in one line — don't debate it.

**Write their request down** so it isn't lost: add it to `~/Documents/Claude/Tasks/` as a short note, and mention it at the end: "You asked about X earlier — that's saved in your Tasks folder, and it's the perfect first thing to try in a new session."

**The same rule holds after the setup ends** — see **STEP 9**. When you're finished, you send them to a new session; you don't carry on working in this one.

### 📚 Teach as you go — this setup is also their first lesson

They are learning Claude for the first time. **Every time something you do has a lesson attached, drop the lesson in one sentence and move on.** Not a tutorial — one line, in context, then keep working. By the end they should have picked up five or six habits without ever feeling taught.

**The lessons worth planting, and when:**

| When it comes up | The one line to say |
|---|---|
| They ask for unrelated work mid-setup | "One session per job — start a new session for a new task and I'll be faster and sharper at it." |
| You finish the interview and save their answers | "I've written this down, so you never have to explain who you are again — every future session already knows." |
| You create the `/skill-name` shortcuts | "Type `/` any time to see your shortcuts — it's quicker than describing what you want." |
| You turn on auto mode | "I'll get on with normal work now instead of asking permission for every step — but I'll always stop and ask before anything risky." |
| They give you a vague answer in the interview | "The more specific you are with me, the better I do — vague question, vague answer." |
| You put a document in their `Context/` folder | "Anything you drop in this folder, I can read later. It's how you give me background without re-explaining." |
| At the very end | "If I ever get something wrong, just tell me — correcting me in the moment works better than starting over." |
| At the very end (STEP 9) | "One session, one job — start a new session for your real work and I'll be sharper and faster at it." |

**Don't lecture, don't batch them into a lesson at the end, and don't say all seven if only three came up naturally.**

### 🔴 How to talk to them — this is their FIRST time using Claude

Assume they have never used Claude, never opened a terminal, and have never heard a single one of the words in this file. Everything you say out loud must pass this test: **would an 18-year-old with no tech background understand it, first read, without asking what a word means?**

**Four rules for every single thing you say to them:**

1. **No jargon, ever. Not even once, not even in passing.** If a technical word is unavoidable, say what it does in the same breath — plain words first, name second.
2. **Short.** One or two sentences per message. They are already overwhelmed. A wall of text makes them stop reading and get lost.
3. **Say what it does FOR THEM, not what it is.** They don't care what a thing is called. They care what changes for them.
4. **Never ask them a question they can't possibly answer.** If it's a technical decision, make the call yourself and tell them what you picked in one line. Only ask about things that live in their head — their name, their job, their company, what they want help with.

**Words they will not understand — never say these to them:** CLI, install the CLI, repo, repository, hook, SessionStart, symlink, junction, LaunchAgent, watcher, daemon, JSON, settings.json, path, directory, terminal, shell, script, sync, config, permissions mode, slash command, trigger, package, `.skill` file, API, OAuth, token, MCP, connector, extension, headless, scrape, environment variable.

**Say it like this instead:**

| ❌ Never say | ✅ Say this |
|---|---|
| "Installing the Google Workspace CLI" | "I'm setting things up so I can read and write your Gmail and Google Calendar for you." |
| "I'll wire up the slash command triggers for your skills" | "I'm adding shortcuts. Later you'll be able to type `/` and pick a task from a list instead of explaining it." |
| "Adding a SessionStart hook to settings.json" | "I'm setting it up so this stays up to date on its own. Nothing for you to do." |
| "Creating a symlink to the canonical skills folder" | "I'm connecting two folders so they can see each other." |
| "Enabling auto mode in permissions" | "I'll get on with normal work instead of asking you to approve every step. I'll still ask before anything risky." |
| "Running the OS path normalization script" | "I'm making sure everything points at the right place on your computer." |
| "The watcher failed to load" | *(say nothing — it doesn't affect them; just move on)* |

**Don't narrate the plumbing at all.** They don't need a play-by-play of STEPs 0 through 4 — it means nothing to them and it makes the setup feel scary and long. One short line when you start ("Setting things up — this takes a few minutes, I'll ask you some questions in a bit"), then quiet work, then the questions. Save the explaining for the end.

### 🔴 Never tell them to install Git or Homebrew

**Git is already installed. Do not check for it, do not mention it, do not offer to install it, and never surface a "git is required" message.** The only way you are reading this file at all is inside Claude Code, which does not start without Git — so it is there by definition.

**Homebrew is not part of this setup either.** Don't install it, don't ask about it, and don't tell the user to. If some later step genuinely needs a tool that isn't on the machine, install that one tool the quietest way that works and only mention it if it fails.

### Where paths in this file point

Every bundle path written below (`Setup Files/setup-os-paths.py`, `Claude/Memory/`, `.claude/CLAUDE.md`, …) is **relative to the bundle root** — the folder that contains this `Setup Files` folder. This file lives one level down, inside `Setup Files/`. Work out the real absolute path on this machine before running anything.

### Which Claude is this for? (read once)

This works with **both** Claude products — but different pieces apply to each. Don't assume; check which the user has and tell them what you skip and why.

- `.claude/CLAUDE.md` (global instructions) → read by **Claude Code** (the terminal/CLI). Skip if they only use the desktop app, but still place it in case they add Claude Code later.
- **The bundled skills** (in `Skills/`) → plain folders that work in **Claude Code**; STEP 3b turns each into a `/skill-name` shortcut. A few of their internal mechanics only matter in the desktop app, which is harmless.
- `Context/` **+** `Memory/` (the knowledge base) → read by **whichever** Claude you point at `~/Documents/Claude/`. Useful in both.

### How to run this without losing your place (this is a long setup)

This is a multi-step job and the machine may be slow. Stay organized so you finish start-to-finish:

1. **First, build a checklist with** `TaskCreate` — one item per STEP below (0, 0b, 1, 1b, 2, 2b, 3, 3b, 4, 5, 6, 6b, 7, 8, 9). This is your map.
2. **Work strictly top to bottom, one step at a time.** Mark a step complete **only after you verify it actually happened** (the folder exists, the file has the content, the link resolves).
3. **Keep each action small.** Don't try to do everything in one giant command. Copy, check, then continue.
4. **If you get interrupted or restarted:** re-open this file, then look at the disk to see what's already done (Does `~/Documents/Claude/` exist? Does `~/.claude/CLAUDE.md` have the rules? Is the skill installed?). Resume from the first step that isn't finished — don't redo completed work.
5. **If a step fails:** don't pretend it's done. But **don't stall the whole setup on it either** — do the rest of the steps first, then tell them at the end, in one plain sentence, what didn't work and what it means for them. A step marked **OPTIONAL** never gets reported at all; just skip it.
6. **Nothing in this setup is allowed to leave them stuck watching you struggle.** If a step is fighting you, take the simpler path or skip it. A finished setup missing one optional convenience beats a half-finished one they abandoned.

---



## STEP 0 — Detect the operating system FIRST (before anything else)

**Your very first action:** figure out whether this is a **Mac**, a **Windows PC**, or **Linux**. Check the platform (e.g. `uname` on Mac/Linux, or the environment on Windows). Then follow the matching column in **every** step below. The instructions are written Mac-first; on Windows, substitute the paths and commands.


| Concept                         | Mac / Linux                                             | Windows                                                      |
| ------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| Home folder (`~`)               | `/Users/<username>/` (Mac), `/home/<username>/` (Linux) | `C:\Users\<username>\`                                       |
| Knowledge base                  | `~/Documents/Claude/`                                   | `C:\Users\<username>\Documents\Claude\`                      |
| Global Claude Code instructions | `~/.claude/CLAUDE.md`                                   | `C:\Users\<username>\.claude\CLAUDE.md`                      |
| Installed Claude app skills     | `~/Library/Application Support/Claude/` (Mac)           | `C:\Users\<username>\AppData\Roaming\Claude\`                |
| Make a folder shortcut          | symlink: `ln -s <target> <link>`                        | junction: `mklink /D <link> <target>` (or a `.lnk` shortcut) |
| Copy a folder                   | `cp -R <src> <dest>`                                    | `xcopy /E /I <src> <dest>` or `Copy-Item -Recurse`           |


**On Windows, the** `Claude` **folder goes in the real per-user Documents folder:** `C:\Users\<username>\Documents\Claude\`**.**

- Replace `<username>` with the actual Windows account name — find it with `echo %USERNAME%` (Command Prompt) or `$env:USERNAME` (PowerShell). Don't hardcode the literal text `<username>`.
- Do **not** use a `%USERPROFILE%\Documents` path blindly: if Documents has been redirected to OneDrive (`C:\Users\<username>\OneDrive\Documents`), still create the `Claude` folder under the plain `C:\Users\<username>\Documents\Claude\` unless the user explicitly says they want it in their OneDrive Documents. Confirm with the user if both folders exist.

**Tell the user which OS you detected** and that you'll adapt everything to it. When you're unsure where something lives on this machine, **search for it** instead of guessing.

---



## STEP 0b — Make sure they can actually SEE their Documents folder (Mac — do this before STEP 1)

**This bit the last group hard: on several Macs the `Documents` folder was flagged hidden, so after setup finished the user could not find a single file you created.** Fix it now, silently, before you copy anything. Don't ask, don't explain, don't make them type anything — they will get lost in a terminal.

**Mac / Linux — run these yourself:**

1. **Unhide it. Just run this — it is harmless if it was never hidden:**
  ```bash
   chflags nohidden ~/Documents
  ```
2. **Confirm it's really visible.** `ls -lO ~ | grep Documents` — the flags column must NOT contain `hidden`. If it still says `hidden`, run the command again and check once more.
3. **Confirm the folder actually exists at that path**, and isn't a stub:
  ```bash
   ls -la ~/Documents
  ```

**Then check where `Documents` really lives — three cases:**

| What you find | What to do |
|---|---|
| `~/Documents` is a normal folder | Normal case. Use it. |
| `~/Documents` is a **symlink**, or `ls ~` shows the real one under **OneDrive** (`~/OneDrive/Documents`, `~/Library/CloudStorage/OneDrive-*/Documents`) | The user's Documents has been redirected into OneDrive. **Ask them, in plain words:** "I'm about to create a Claude folder for your files. Do you want it in your normal Documents folder, or the one that syncs with OneDrive?" Then use whichever they pick, and use that same path everywhere else in this file. |
| Desktop & Documents are synced to **iCloud Drive** (`~/Library/Mobile Documents/com~apple~CloudDocs/Documents`) | `~/Documents` still works as the everyday path — use it, but note it for yourself, because background helpers can't always reach iCloud paths (see STEP 3b, part 3). |

**If the user's knowledge base ends up somewhere other than `~/Documents/Claude/`, that new path replaces `~/Documents/Claude/` everywhere in this file** — including inside the scripts in STEP 3b and the "My Knowledge Base" section in STEP 2.

**Windows:** hidden-Documents isn't the same problem, but the OneDrive redirect is — see the STEP 0 Windows note above, and settle it the same way: ask them in plain words which one they want.

**Say to them, once, only if you had to change something:** "Your Documents folder was hidden on this Mac — I've made it visible again so you can find your files." Nothing more.

---



## STEP 1 — Copy the structure to `~/Documents/Claude/`

Reproduce this bundle's `Claude/` folder under the user's Documents. Create parent folders as needed. The paths below are written Mac-style (`~/Documents/Claude/`) — **on Windows, every** `~/Documents/Claude/` **below means** `C:\Users\<username>\Documents\Claude\` (the real per-user Documents folder; see the STEP 0 Windows note).


| In this bundle                                                       | Copy it to                                 |
| -------------------------------------------------------------------- | ------------------------------------------ |
| `Claude/CLAUDE.md`                                                   | `~/Documents/Claude/CLAUDE.md`             |
| `Claude/Context/` (with `Company/`, `Personal/`, their `CLAUDE.md`s) | `~/Documents/Claude/Context/`              |
| `Claude/Memory/` (all the `.md` files, plus the `HTML Files/` subfolder) | `~/Documents/Claude/Memory/`               |
| `Claude/Skills/` (the whole folder — every skill subfolder **plus** its own `CLAUDE.md` and `MEMORY.md`) | `~/Documents/Claude/Skills/` |
| `Claude/Scheduled/` (its own `CLAUDE.md` — ships otherwise empty)    | `~/Documents/Claude/Scheduled/`            |
| `Claude/Tasks/` (ships empty — just create the folder)               | `~/Documents/Claude/Tasks/`                |


Every folder keeps the same name it has here — the global `CLAUDE.md` expects these exact paths, so they resolve as-is. **If a destination already exists, tell the user and ask before overwriting** — don't clobber work they already have.

After copying, the five working folders under `~/Documents/Claude/` are:

- `Context/` — durable docs about the user and their company.
- `Memory/` — all memory files (one per topic, or one subfolder per topic when it ships companion files — e.g. `HTML Files/`).
- `Skills/` — the skills.
- `Scheduled/` — one subfolder per scheduled routine, once the user creates any. `Scheduled/CLAUDE.md` is the shared rulebook every routine follows — never edit it for a single routine.
- `Tasks/` — one subfolder per ongoing working job. Starts empty; anything the user asks for mid-setup gets parked here (see the HARD RULE at the top).

---

## STEP 1b — Make the copied files match this operating system

Several of the files just copied ship BOTH a Mac/Linux and a Windows version of certain rules,
wrapped in HTML comments so they're invisible when the Markdown renders:

```
<!--os:mac--> ... <!--/os:mac-->
<!--os:win--> ... <!--/os:win-->
```

Run the bundle's `Setup Files/setup-os-paths.py` against the copied destination, passing the OS
detected in STEP 0:

```bash
python3 "Setup Files/setup-os-paths.py" mac  ~/Documents/Claude          # Mac/Linux
python  "Setup Files/setup-os-paths.py" win  "C:\Users\<username>\Documents\Claude"   # Windows
```

This deletes the other OS's blocks, unwraps the surviving side's markers, and — on Windows —
rewrites any leftover `~/Documents/Claude/...`-style paths to the Windows form. It's safe to
re-run; a second pass changes nothing.

**Verify it worked:** search the copied folder for `<!--os:` — zero hits is the only passing
result.

```bash
grep -rn "<!--os:" ~/Documents/Claude                                    # Mac/Linux
```
```powershell
Get-ChildItem -Recurse "$env:USERPROFILE\Documents\Claude" | Select-String "<!--os:"   # Windows
```

If anything remains, the OS argument was wrong or a file wasn't included; fix it before moving on.

---



## STEP 2 — Merge the global instructions (`~/.claude/CLAUDE.md`)

This bundle's `.claude/CLAUDE.md` is the global **Claude Code** instruction file (best-practice rules + the folder layout above). It belongs in the per-user home `.claude` folder:

- **Mac/Linux:** `~/.claude/CLAUDE.md`
- **Windows:** `C:\Users\<username>\.claude\CLAUDE.md`

In the two bullets below, `~/.claude/CLAUDE.md` means that Windows path on a PC.

- **If the user already has a global** `CLAUDE.md` **there:** **merge** — don't replace. Keep their existing instructions, and add any sections from this bundle's file they don't already have (**My Knowledge Base**, **Memory Routers**, **Thinking Partner Mode**, **Response Style**, **Plain English**, **Ground Every Claim in Data**, **Core Principles**, **Verification Before Done**, **File Links**, **Self-Improvement Loop**, **Token Conservation**, **Git**, **Finding & Using Skills**, **Preferred Tools**). If two rules conflict, show the user both and let them choose.
- **If they don't have one:** copy this bundle's `.claude/CLAUDE.md` there as-is (create the `.claude` folder if it doesn't exist).

### ⚠️ The one section you must NOT skip: "My Knowledge Base"

Whether you merge or copy fresh, the finished `~/.claude/CLAUDE.md` **must** contain the **"My Knowledge Base — read it before ANY personal or company work"** section from this bundle's `.claude/CLAUDE.md`. Without it, every future session ignores the `Context/` and `Memory/` files you're about to fill in during STEP 5 — the whole setup goes to waste.

Do this:

1. Open the finished `~/.claude/CLAUDE.md` and search it for `Memory/personal.md`.
2. **If it's not there, add the whole "My Knowledge Base" section** (copy it verbatim from this bundle's `.claude/CLAUDE.md`, near the top of the file).
3. On **Windows**, change the path in that section to `C:\Users\<username>\Documents\Claude\` with the real account name.
4. If the user keeps their knowledge base somewhere other than `~/Documents/Claude/`, update the paths in that section to the real location — in that section AND everywhere else in the file (`Memory/task-delegation.md`, `Memory/self-improvement.md`, `Memory/website-crawling.md`, `Memory/mcp-connectors.md`, `Memory/routines.md`, `Memory/HTML Files/`, `Scheduled/`, `Skills`).
5. **Verify by reading the file back** and confirming the section is really there. Don't mark this step done otherwise.

### 🔴 Then OS-strip this file too — it is NOT covered by STEP 1b

`~/.claude/CLAUDE.md` lives outside `~/Documents/Claude/`, so the STEP 1b run never touched it — and it
ships the same `<!--os:mac-->` / `<!--os:win-->` blocks. Leave them and the user's global instructions
carry **both** operating systems' rules plus visible comment markers, forever. Run the script again,
now that the file is in place:

Point it at **the one file**, not the folder — `~/.claude/` also holds installed plugins, skills and
commands, and the script rewrites every `.md` and `.py` it is given:

```bash
python3 "Setup Files/setup-os-paths.py" mac ~/.claude/CLAUDE.md                      # Mac/Linux
```
```powershell
python "Setup Files\setup-os-paths.py" win "$env:USERPROFILE\.claude\CLAUDE.md"      # Windows
```

**Verify:** searching `~/.claude/CLAUDE.md` for `<!--os:` must return zero hits. If the user **merged**
into an existing file, check the merged result — markers can survive a hand-merge even after the script runs.

---



## STEP 2b — Turn on **auto mode** for every session (`~/.claude/settings.json`)

Auto mode lets Claude Code run safe, ordinary work without stopping to ask permission for every single tool call. It's a **one-line setting** and it applies to every session on this computer, forever.

**The file:**

- **Mac/Linux:** `~/.claude/settings.json`
- **Windows:** `C:\Users\<username>\.claude\settings.json`

**The setting:** inside the top-level `"permissions"` object, add `"defaultMode": "auto"`.

A minimal correct file looks like this:

```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

**How to do it — merge, never overwrite:**

1. **Back it up first:** copy `settings.json` to `settings.json.bak` before touching it. If the file doesn't exist yet, create it with exactly the JSON above and skip to step 5.
2. **Read the existing file.** It probably already has `env`, `hooks`, `permissions.allow`, `enabledPlugins`, etc. **Keep all of it.**
3. **If a** `"permissions"` **object already exists,** add the single `"defaultMode": "auto"` line inside it — alongside `"allow"`, not replacing it. If `permissions.defaultMode` is already set to something else (`"default"`, `"plan"`, `"acceptEdits"`), **tell the user what it is now and ask before changing it.**
4. **If there's no** `"permissions"` **object,** add the whole thing as a new top-level key.
5. **Check the JSON is still valid** — a stray comma breaks every future session. Run `python3 -m json.tool ~/.claude/settings.json` (Mac/Linux) or `Get-Content $env:USERPROFILE\.claude\settings.json | ConvertFrom-Json` (Windows). If it errors, restore the `.bak` and try again.
6. **Read the file back** and confirm `"defaultMode": "auto"` is really there. Then tell the user: **it takes effect the next time they start Claude Code**, not in the current session.

**Two things NOT to do:**

- ❌ **Don't edit anything in** `~/.claude/sessions/`. Those `<pid>.json` files are temporary per-window state (process id, working folder, session id) that Claude Code rewrites on every launch — changes there are wiped instantly and do nothing.
- ❌ **Don't put this in** `settings.local.json`. That file is per-project; this setting belongs in the global `settings.json` so it covers every session.

**Say this to the user in plain English:** "Auto mode is on — I'll get on with normal work instead of asking you to approve every step. I'll still stop and ask before anything risky, like deleting files, sending messages, or spending money. You can turn it off any time by changing `defaultMode` back to `default` in that file."

---



## STEP 3 — Wire up the skills folder + the "Skills - Claude Cowork" shortcut

Every Claude desktop install ships with a `skill-creator` skill — use it as the landmark to find the **canonical skills folder** on this machine. Search the app-support location for a `skill-creator` folder/skill:

- **Mac:** look under `~/Library/Application Support/Claude/` (skills usually live in a `skills/` subfolder there).
- **Windows:** look under `%APPDATA%\Claude\`.

Once you've found the folder that contains `skill-creator`, that's the canonical skills folder.

**Make a shortcut to it inside** `~/Documents/Claude/` **named** `Skills - Claude Cowork` (symlink on Mac, junction/`.lnk` on Windows), so Claude can reach the app's installed skills from the knowledge base. This sits alongside the copied `Skills/` folder — two different things: `Code` = the skills shipped in this bundle; `Cowork` = a shortcut to the app's installed skills.

If this machine only has Claude Code (no desktop app / no `skill-creator` folder), say so and skip the shortcut — the bundled skill folders under `Skills/` still work as plain folders either way.

Tell the user what you found, in plain words: "I connected two folders so Claude can see all your skills in one place."


---



## STEP 3b — Auto-generate a slash command for every Claude Code skill

> 🔴 **This is the step that got stuck most often last time.** Parts 1, 2 and 4 are required; part 3 is optional and you abandon it the moment it resists. Nothing here is worth stalling the setup over.

Goal: give the user a `/skill-name` slash command for **every** skill folder in `~/Documents/Claude/Skills/`, so any new skill they add later shows up as a new shortcut **the next time they open Claude Code**.

Three pieces, in priority order: (1) a **sync script** that turns each skill folder into a command file, (2) a **SessionStart hook** that runs that script every time Claude Code starts, and (3) an **optional** background watcher.

> 🔴 **Parts 1, 2 and 4 are required. Part 3 is optional and you must not get stuck on it.** "Shortcuts refresh when you restart Claude" is the whole promise here, and parts 1+2+4 deliver it completely. Part 3 only removes the restart, and it is the step that fails most often on other people's computers. **The moment it resists, abandon it and move on — silently.**

### 1. Create the sync script

Write this to `~/.claude/scripts/sync-skills-to-commands.sh` (create the `scripts` folder if needed) and make it executable (`chmod +x`). It scans the skills folder and writes one command file per skill into `~/.claude/commands/`:

```bash
#!/bin/bash
set -euo pipefail

SKILLS_DIR="$HOME/Documents/Claude/Skills"
COMMANDS_DIR="$HOME/.claude/commands"

# Skill folders to NOT turn into commands (add names here as needed)
IGNORE=("0-template")

mkdir -p "$COMMANDS_DIR"
[ -d "$SKILLS_DIR" ] || exit 0

for skill_path in "$SKILLS_DIR"/*; do
  [ -d "$skill_path" ] || continue
  skill="$(basename "$skill_path")"

  skip=false
  for ignored in "${IGNORE[@]}"; do
    [ "$skill" = "$ignored" ] && skip=true && break
  done
  [ "$skip" = true ] && continue

  # Only treat it as a skill if it actually has a SKILL.md somewhere inside
  [ -n "$(find "$skill_path" -maxdepth 2 -iname 'SKILL.md' -print -quit)" ] || continue

  cat > "$COMMANDS_DIR/$skill.md" <<EOC
Use the skill in \`~/Documents/Claude/Skills/$skill/\`.

Read that skill's \`SKILL.md\` first, then apply it to the user's request below.
EOC
done
```

> ⚠️ **If the knowledge base is NOT at `~/Documents/Claude/`** (see STEP 2, item 4), edit `SKILLS_DIR` at the top of this script **and** the path inside the `cat > ... <<EOC` block below to the real location — both, or the commands point at a folder that isn't there.

Each generated `.md` file's **name IS the slash command** — e.g. a folder named `new-skill` becomes `/new-skill`. Re-running is safe: it just rewrites the files, adding any new skills and leaving existing ones current.

### 2. Wire it to run on every Claude Code startup (SessionStart hook)

Add a `SessionStart` hook to `~/.claude/settings.json` that runs the script. **Merge** — if the user already has a `hooks.SessionStart` array, append this entry, don't overwrite theirs:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$HOME/.claude/scripts/sync-skills-to-commands.sh\" 2>/dev/null || true",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

This covers "new skill appears the next time they open Claude Code."

### 3. OPTIONAL — run the instant a skill is added (file watcher)

> 🔴 **STOP. Read this before you touch anything in part 3.**
>
> **This part is optional and it is the single most common place this setup gets stuck.** Parts 1, 2 and 4 above are the real feature — they give the user working `/skill-name` shortcuts, refreshed every time Claude Code starts. That is enough. Part 3 only removes the need to restart, which nobody actually minds.
>
> **You get ONE attempt, plus at most one offer of help.** If it doesn't work first try, you may make the single Full Disk Access offer described at the bottom of this part — **once**, phrased as optional. Beyond that: delete whatever you half-created, say nothing more about it, and go straight to part 4. **Do not debug it. Do not retry with a different approach. Do not say the words "watcher", "LaunchAgent", "daemon" or "scheduled task" to them at any point** — a failure here changes nothing they will ever notice.
>
> **Skip part 3 entirely, without even attempting it, if either of these is true:**
> - The knowledge base is inside **iCloud Drive**, **OneDrive**, **Dropbox**, or any other synced folder — background helpers can't reliably reach those, and the sync engine fires the watcher constantly for no reason.
> - You already spent more than about two minutes on it.
>
> In either case the honest outcome is: the shortcuts work, they refresh on restart, done.

If none of those apply and you want the one attempt, here it is.

**Mac — a LaunchAgent, built into macOS.** Write this to `~/Library/LaunchAgents/com.claude.sync-skills.plist`, substituting the real absolute paths (no `~`, no `USERNAME` left in the file — `launchd` expands neither):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.claude.sync-skills</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/USERNAME/.claude/scripts/sync-skills-to-commands.sh</string>
  </array>
  <key>WatchPaths</key>
  <array>
    <string>/Users/USERNAME/Documents/Claude/Skills</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
</dict>
</plist>
```

**Before loading it, check these three things — each one is a silent failure if you skip it:**

1. **The watched folder must already exist.** `WatchPaths` pointing at a missing folder makes the agent do nothing, forever, with no error. STEP 1 should have created it — verify, don't assume.
2. **Both paths must be real absolute paths.** If the literal text `USERNAME` or a `~` survives into the file, it fails silently.
3. **The file must be valid.** `plutil -lint ~/Library/LaunchAgents/com.claude.sync-skills.plist` — anything but `OK` means stop and skip to part 4.

**Load it with the modern command** (`launchctl load` is deprecated and returns confusing errors on current macOS):

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claude.sync-skills.plist
```

If it says it's already loaded, remove it with `launchctl bootout gui/$(id -u)/com.claude.sync-skills` and bootstrap once more — **that is your one retry, and only for that specific "already loaded" message.**

**Confirm it actually registered:** `launchctl list | grep com.claude.sync-skills` must print a line. If it prints nothing, or the middle column is a non-zero number, **it didn't work** — clean up and move on:

```bash
launchctl bootout gui/$(id -u)/com.claude.sync-skills 2>/dev/null
rm -f ~/Library/LaunchAgents/com.claude.sync-skills.plist
```

### If macOS blocks it — offer the easy fix once, then let it go

**The usual reason this fails on a Mac:** `~/Documents` is privacy-protected by macOS, so a background helper reading it gets blocked until Full Disk Access is switched on.

**You cannot grant this yourself.** macOS deliberately requires a human to flip the switch — no command, no script, and no amount of the user typing "I approve" in this chat can do it, because the approval has to happen in the system's own window where macOS knows a real person is clicking. **Never pretend otherwise, and never ask them to type an approval to you as if that would work.**

**What you CAN do is make it a 15-second job instead of a scavenger hunt.** Offer it once, in plain words:

> "One small optional thing — macOS is blocking a background helper from seeing your Documents folder. I can open the right settings page for you; it's one switch to flip and it takes about fifteen seconds. Worth doing, or shall I skip it? Everything works either way."

**If they say yes**, open the exact page — don't make them hunt through System Settings:

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

Then give them **one instruction at a time**, waiting between each:

1. "The window that just opened is **Full Disk Access**."
2. "Find **Terminal** in that list and switch it on." *(If it isn't listed, click the **+** button, then pick Terminal from Applications → Utilities.)*
3. "It'll ask for your Mac password — that's normal, and the typing stays invisible."

Then retry the load **once**. If it still fails, say: **"No luck — but it changes nothing you'll notice, everything's working."** and move on.

**If they say no, or hesitate at all, drop it instantly.** Say "no problem, skipping it" and move on. Parts 1, 2 and 4 already do the job — this is a convenience, not a feature.

**Windows:** the same one-attempt rule applies — see the **Windows** section at the end of this step. If registering the scheduled task needs an admin window, **skip it silently.**

**What to tell the user about part 3:** nothing. If it worked, it's invisible. If it didn't, it's equally invisible.

### 4. Run it now — so the bundled skills become commands the moment they install

Do this **during setup, right after STEP 1** has copied the bundle's skills into `~/Documents/Claude/Skills/`. Run the sync script once by hand:

```bash
bash "$HOME/.claude/scripts/sync-skills-to-commands.sh"
```

That single run instantly creates a `/skill-name` slash command for **every** skill the installer just dropped into that folder (each unpacked skill folder that has a `SKILL.md` — e.g. `/skill-builder-protocol`, `/process-interviewer`, `/the-humanizer`). So the user has working slash commands the moment setup finishes — they don't have to add anything or wait for a restart. Then tell the user how many command files it wrote and list them.

> Note: the `0-template` scaffold and any `.skill` **package** file are intentionally skipped — only unpacked folders containing a `SKILL.md` become slash commands.

### Windows

Same three layers as Mac, in PowerShell. Paths use `$env:USERPROFILE` (that's `C:\Users\<username>\`) so they work for any account.

**1. The sync script.** Save to `%USERPROFILE%\.claude\scripts\sync-skills-to-commands.ps1`:

```powershell
$SkillsDir   = Join-Path $env:USERPROFILE 'Documents\Claude\Skills'
$CommandsDir = Join-Path $env:USERPROFILE '.claude\commands'
$Ignore      = @('0-template')

New-Item -ItemType Directory -Force -Path $CommandsDir | Out-Null
if (-not (Test-Path $SkillsDir)) { return }

Get-ChildItem -Path $SkillsDir -Directory | ForEach-Object {
    $skill = $_.Name
    if ($Ignore -contains $skill) { return }
    # Only treat it as a skill if it has a SKILL.md somewhere inside
    if (-not (Get-ChildItem -Path $_.FullName -Recurse -Depth 1 -Filter 'SKILL.md' -File -ErrorAction SilentlyContinue | Select-Object -First 1)) { return }

    $body = @"
Use the skill in ``~/Documents/Claude/Skills/$skill/``.

Read that skill's ``SKILL.md`` first, then apply it to the user's request below.
"@
    Set-Content -Path (Join-Path $CommandsDir "$skill.md") -Value $body -Encoding UTF8
}
```

**2. Run on Claude Code startup.** In `settings.json`, set the SessionStart hook `command` to:
`powershell -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\.claude\scripts\sync-skills-to-commands.ps1"`

**3. OPTIONAL — run the instant a skill is added (watcher).**

> 🔴 **Same one-attempt rule as the Mac version above.** `Register-ScheduledTask` normally needs an **administrator** PowerShell window. Most people are admins on their own laptop, so this usually works — but if Windows refuses, or it errors for any reason, **skip it: delete anything you half-created, say nothing, and go to part 4.** Parts 1, 2 and 4 already give them working shortcuts that refresh on restart. **Never walk a non-technical user through opening an admin terminal themselves** — either it works when you run it, or it doesn't happen.

Save this watcher to `%USERPROFILE%\.claude\scripts\watch-skills.ps1` — it runs the sync whenever the skills folder gains or loses a subfolder, no restart needed:

```powershell
$SkillsDir = Join-Path $env:USERPROFILE 'Documents\Claude\Skills'
$Sync      = Join-Path $env:USERPROFILE '.claude\scripts\sync-skills-to-commands.ps1'

& $Sync   # sync once on launch

$fsw = New-Object System.IO.FileSystemWatcher $SkillsDir
$fsw.IncludeSubdirectories = $false
$fsw.EnableRaisingEvents = $true
$action = { Start-Sleep -Milliseconds 500; & $using:Sync }
Register-ObjectEvent $fsw Created -Action $action | Out-Null
Register-ObjectEvent $fsw Deleted -Action $action | Out-Null
Register-ObjectEvent $fsw Renamed -Action $action | Out-Null
while ($true) { Start-Sleep -Seconds 3600 }
```

Register the watcher to start at logon so it's always running. In an **admin** PowerShell:

```powershell
$act = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "%USERPROFILE%\.claude\scripts\watch-skills.ps1"'
$trg = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName 'ClaudeSyncSkills' -Action $act -Trigger $trg -RunLevel Limited
```

**Simplest fallback, and the right default:** skip the watcher entirely and rely on the startup hook from part 2. The shortcuts refresh every time they open Claude Code, which is all anyone actually needs. (If you want a middle ground that needs no admin rights, Task Scheduler can run the **sync** script daily with `New-ScheduledTaskTrigger -Daily -At 9am` — but don't spend time on it.)

**4. Run it now (during install).** After STEP 1 copies the skills, run the sync once so the bundled skills become commands immediately:
`powershell -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\.claude\scripts\sync-skills-to-commands.ps1"`

The same **honest caveat** applies as on Mac: the watcher gets the command file onto disk immediately; whether an already-open Claude session shows the new `/command` before its next start depends on how Claude Code loads commands.

---



## STEP 3c — Install the seven safety checks (`~/.claude/hooks/`)

These are seven small scripts that watch what Claude does and stop it before it makes a
mess. **They are the difference between a Claude that can quietly break something and one
that catches itself.** Do this after STEP 3b and before STEP 4.

⚠️ **Never use the word "hook" with them.** In their words: *"I'm adding some safety checks
so Claude catches its own mistakes before they reach you. Nothing for you to do."*

### What each one does, so you can decide if one is failing

| File | Stops |
|---|---|
| `dangerous-bash-guard.sh` | Destructive commands — wiping folders, force-deleting work, overwriting shared branches. **The most important one.** |
| `check-file-links.py` | Claude handing them a link to a file that isn't there. They click, nothing opens, they assume Claude is broken |
| `check-terminal-cwd.py` | Claude handing them a command that will fail from the folder they're actually in |
| `check-fetch-giveup.py` | Claude saying "I can't open that page" without having really tried |
| `lesson-detector.sh` | Nothing — it's the one that *adds*. It spots "you got that wrong" and makes Claude write the lesson down instead of forgetting it |
| `check-deferred-learnings.py` | Claude telling them about a lesson instead of just saving it |
| `check-durable-rule-edits.py` | A new rule landing in their instructions or memory without Claude checking it's worth keeping |

🔴 **Tell them ONE thing about these, once, in plain words:** *"Sometimes Claude will answer,
then correct itself and answer again. That's one of these checks doing its job — it's not a
glitch."* Without that sentence the first double-reply looks broken.

### Mac

**1. Copy the files.** They're bundled in `Setup Files/For Mac/hooks/`:

```bash
mkdir -p "$HOME/.claude/hooks"
cp "<setup-folder>/Setup Files/For Mac/hooks/"*.py "$HOME/.claude/hooks/"
cp "<setup-folder>/Setup Files/For Mac/hooks/"*.sh "$HOME/.claude/hooks/"
chmod +x "$HOME/.claude/hooks/"*.sh "$HOME/.claude/hooks/"*.py
```

**2. Check the two things they depend on**, before you wire anything up:

```bash
command -v jq        # needed by dangerous-bash-guard.sh and lesson-detector.sh
python3 --version    # needed by the five .py checks
```

- **`jq` missing** is unusual — macOS has shipped it at `/usr/bin/jq` since Monterey. If it
  really is absent, skip `dangerous-bash-guard.sh` and `lesson-detector.sh` and install the
  five Python ones. ⛔ **Do not tell them to install Homebrew.**
- 🔴 **`python3` may open an Apple dialog** offering to install developer tools. On a fresh
  Mac that dialog is the FIRST sign of trouble, and it is not one they can be walked
  through. **If it appears: cancel it, install only `dangerous-bash-guard.sh` and
  `lesson-detector.sh`, and say nothing about the rest.** Five missing checks is a fine
  outcome; a confused user staring at an Xcode installer is not.

**3. Merge into `~/.claude/settings.json`.** ⚠️ **Merge, never overwrite** — STEP 3b already
put a `SessionStart` entry in `hooks`, and that must survive. Append to the arrays that exist
and create only the ones that don't:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$HOME/.claude/hooks/dangerous-bash-guard.sh" }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "bash \"$HOME/.claude/hooks/lesson-detector.sh\" 2>/dev/null || true", "timeout": 10 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python3 \"$HOME/.claude/hooks/check-file-links.py\"", "timeout": 15 },
          { "type": "command", "command": "python3 \"$HOME/.claude/hooks/check-terminal-cwd.py\"", "timeout": 15 },
          { "type": "command", "command": "python3 \"$HOME/.claude/hooks/check-fetch-giveup.py\"", "timeout": 15 },
          { "type": "command", "command": "python3 \"$HOME/.claude/hooks/check-deferred-learnings.py\"", "timeout": 15 },
          { "type": "command", "command": "python3 \"$HOME/.claude/hooks/check-durable-rule-edits.py\"", "timeout": 15 }
        ]
      }
    ]
  }
}
```

🔴 **Add `check-durable-rule-edits.py` LAST, and only after STEP 2 is finished.** It fires
whenever something writes a rule into `~/.claude/CLAUDE.md` — which is exactly what STEP 2
does. Wired up early, it blocks your own setup.

### Windows

**1. Copy the files** from `Setup Files/For PC/hooks/`:

```powershell
$dst = Join-Path $env:USERPROFILE '.claude\hooks'
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item "<setup-folder>\Setup Files\For PC\hooks\*" -Destination $dst -Force
```

**2. Check for Python:** `python --version` or `py --version`. If neither answers, **install
none of the `.py` checks** — go straight to `lesson-detector.ps1`, which needs nothing but
PowerShell. ⛔ Do not tell them to install Python.

**3. Merge into `settings.json`**, same merge rule as Mac. Use whichever of `python` or `py`
answered in step 2:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "powershell -NoProfile -ExecutionPolicy Bypass -File \"%USERPROFILE%\\.claude\\hooks\\lesson-detector.ps1\"", "timeout": 10 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python \"%USERPROFILE%\\.claude\\hooks\\check-file-links.py\"", "timeout": 15 },
          { "type": "command", "command": "python \"%USERPROFILE%\\.claude\\hooks\\check-terminal-cwd.py\"", "timeout": 15 },
          { "type": "command", "command": "python \"%USERPROFILE%\\.claude\\hooks\\check-fetch-giveup.py\"", "timeout": 15 },
          { "type": "command", "command": "python \"%USERPROFILE%\\.claude\\hooks\\check-deferred-learnings.py\"", "timeout": 15 },
          { "type": "command", "command": "python \"%USERPROFILE%\\.claude\\hooks\\check-durable-rule-edits.py\"", "timeout": 15 }
        ]
      }
    ]
  }
}
```

⛔ **`dangerous-bash-guard.sh` is NOT installed on Windows, and there is no substitute in
this template.** It is 267 lines of bash and needs `jq`; neither exists on a stock Windows
machine, and the file this template refuses to make them install is exactly what would
provide them. **Say nothing to the user about it.** ⚠️ **It is also the most valuable of the
seven, so a Windows setup is genuinely less protected than a Mac one** — worth knowing when
one of them breaks something and the other doesn't.

⚠️ **The `.py` checks on Windows have not been run on a real Windows machine.** The paths in
them accept both `\` and `/`, but treat the first Windows install as the test: if a check
misbehaves, remove that one line from `settings.json` and carry on. **One bad check must
never cost them the whole setup.**

### Prove they actually work — do not skip this

A check that is copied but not wired up looks identical to one that is working:

```bash
echo '{"prompt":"you forgot to check that"}' | bash "$HOME/.claude/hooks/lesson-detector.sh"
```

That must print a line of JSON. Silence means it is not wired up. Then ask Claude in a fresh
session to link a file that does not exist — `check-file-links.py` should make it correct
itself. **If neither test does anything, the `settings.json` merge did not take:** re-read the
file and check you appended to the existing `hooks` object rather than replacing it.

---

## STEP 4 — Get Claude for Chrome installed AND signed in (don't let this one slide)

> 🔴 **Before this step, re-read “How to talk to them” at the top of this file.** You are hundreds of lines past it and drift is the failure mode here.

**Most of the last group never installed this, and it's the single biggest thing holding their Claude back.** Without it you can't open pages, sign in to sites, or do anything on the web on their behalf — you're limited to reading simple public pages. **Treat this as required, not optional. Don't move on until it's actually working, or they've clearly said no twice.**

### What you CAN and CANNOT do here

**You cannot install it for them.** Chrome requires a human to click **Add to Chrome** and then confirm in Chrome's own popup — that's a browser security rule, not something you can work around, and you shouldn't try. **You also cannot sign in for them.** What you *can* do is open the page, tell them exactly which button to press, and check whether it worked — so they never have to figure anything out.

### 1. Sell it in one sentence, in plain words

Don't describe an extension. Describe what they get:

> "One more thing worth doing — it takes a minute and it's the difference between me answering questions and me actually doing things for you. It lets me open web pages, fill in forms, look things up on sites you're logged into, and do real tasks in your browser. Want me to open the page?"

### 2. Open the page for them

```bash
open "https://claude.com/claude-for-chrome"          # Mac
```
```powershell
start "https://claude.com/claude-for-chrome"         # Windows
```

Then walk them through it, **one instruction at a time — wait for them to say done before the next one:**

1. "Click the blue **Add to Chrome** button."
2. "Chrome will pop up a small box asking if you're sure — click **Add extension**."
3. "Now click the little puzzle-piece icon at the top right of Chrome, and pin Claude so it stays visible."
4. **"Last bit, and this is the part people miss — click the Claude icon and sign in with the same account you use for Claude."**

### 3. 🔴 Verify they're actually SIGNED IN — installed is not enough

**Installing without signing in is the most common failure, and it looks identical to success from their side.** They will say "done" when they've only added the extension. **Check it yourself — don't take "done" as proof.**

**How to check:** try to use a Chrome browser tool (open a tab, read a page). If the extension isn't there or isn't signed in, the tool returns a "not connected" error. That error IS your answer.

**Then loop until it works — up to three tries:**

- **Not connected at all** → "Almost there — I can't see the extension yet. Can you check the puzzle-piece icon at the top right of Chrome and make sure Claude is listed?" Wait, then check again.
- **Connected but not signed in** → "Nearly done — click the Claude icon in Chrome and sign in with the same email you use for Claude. It only asks once." Wait, then check again.
- **Working** → tell them plainly: "That's working — I can use your browser now."

**Keep checking, don't nag.** One clear instruction, wait, re-check. After three honest attempts, stop, and tell them exactly how to finish it later: "Whenever you get a minute — click the Claude icon in Chrome and sign in. Then I'll be able to use your browser." **Then move on with the setup.** This never blocks the rest.

### 4. Mac only — also add "Control Chrome"

Same approach: it drives their real, logged-in Chrome window for one-off jobs. (On Windows, skip it — Claude for Chrome only.)

> ⚠️ **For you, not for them:** these tools drive the user's *real* Chrome window and **steal focus on every action** — every click yanks their window. They're for **single, one-off interactions**, never bulk loops (resolving dozens of URLs in a row can lock the user out of their own computer). For anything repeatable or multi-step, prefer **headless Playwright** (see `Memory/website-crawling.md`).

**Also tell them the habit, one line:** "When you want me to do something on a website, just say so — I'll use your browser. You'll see it moving; that's me."


---

## STEP 5 — Interview the user (two sets of questions)

> 🔴 **Before this step, re-read “How to talk to them” and “Teach as you go” at the top of this file.** You are hundreds of lines past it and drift is the failure mode here.

Now fill in who they are and what their company does. **Run two short interviews.** Rules for both:

- **Ask 3 at a time, maximum.** Never dump a list of 24 questions on them. Ask three, wait, save, ask three more.
- 🔴 **Reword every question below into everyday English before you ask it.** The lists further down are a checklist for *you* — they are not a script. Several are written in work-jargon that a first-time user will not understand. Rewrite each one the way you'd ask a friend.
- 🔴 **One sentence per question. No explaining why you're asking.** The last group found the questions overwhelming, and it was mostly the extra words.
- **They can stop anytime** — if they say stop/skip/enough, save whatever they've given so far and move on. Partial is fine, and tell them that up front.
- **Save as you go:** personal answers → `~/Documents/Claude/Memory/personal.md`; company answers → `~/Documents/Claude/Memory/company.md`. Keep entries short and durable.
- For anything they don't know or want to skip, leave the placeholder and move on. **Never push twice on the same question.**

**How to reword them — copy this register:**

| ❌ On the list as | ✅ Ask it like this |
|---|---|
| "Output format preferences — bullets vs prose, tables, length limits?" | "Do you like short bullet points, or full sentences?" |
| "How do you like decisions framed — one recommendation, or options?" | "When you ask me something, do you want my one best answer, or a few choices?" |
| "Areas you're NOT expert in and want extra explanation on?" | "Is there anything you'd want me to explain in extra detail, because it's not your area?" |
| "Tools and platforms you live in daily" | "What apps do you use most at work?" |
| "Main goals / OKRs / North Star metric this year?" | "What's the big thing your company is trying to hit this year?" |
| "Positioning — what makes you different from competitors?" | "Why do customers pick you instead of someone else?" |
| "Compliance or legal limits on what can be said publicly?" | "Is there anything you're not allowed to say publicly about your work?" |
| "Privacy boundaries — anything Claude should never store or share?" | "Is there anything you'd rather I never write down?" |

**Open the interview like this, not with a preamble about memory files:**

> "Okay, the setup's done. Now I just want to get to know you a bit so I'm actually useful. About 10 quick questions, and you can say 'skip' to any of them. First: what's your name, and what do you do for work?"



### 🔴 Start by asking for two links — this does most of the interview for them

**Don't ask "can I research you online?"** — it sounds vague and slightly creepy, and it makes them do the thinking. **Ask for the two links instead.** It's concrete, it takes them ten seconds, and it lets you fill in most of both files yourself.

**Ask this first, before any other question:**

> "Quickest way to do this: what's your LinkedIn, and your company's website? I'll read them and fill in most of this myself, then you just correct whatever I got wrong. If you'd rather not, no problem — I'll just ask you instead."

**Then:**

1. **Take whatever they give you.** One link, both, or neither — all fine. If they only have one, use it. If they have neither, skip straight to the questions.
2. **Go read them.** LinkedIn → their role, background, career history, location. Company site → what it does, products, customers, positioning, tone of voice. While you're on the company site, the About and Pricing pages are usually worth more than the homepage.
3. **Draft both profiles from what you found**, then **show them and ask them to correct it** — never save looked-up information as fact without them seeing it:

   > "Here's what I got from those. Tell me anything that's wrong or out of date."

4. **Then only ask the questions the links couldn't answer.** This is the whole point — a good LinkedIn plus a company site can cover 15 of the 24 questions in each list. **Skipping questions you already have answers to is the single biggest thing you can do to stop overwhelming them.**
5. **Say out loud how much time it saved:** "That covered most of it — just a few things left that aren't online."

**If they'd rather not share the links, don't push.** Say "no problem" once and go straight to asking.

### Personal questions (ask at least these ~24)

1. Your full name, and what should Claude call you?
2. Your role/title and what you do day to day?
3. Your company or employer (or are you self-employed)?
4. Location and time zone?
5. What do you mainly want to use Claude for? (top 3–5 tasks)
6. Communication style you prefer — blunt or gentle? short or detailed?
7. Output format preferences — bullets vs prose, tables, length limits?
8. Areas you know deeply / your expertise?
9. Areas you're NOT expert in and want extra explanation on?
10. Tools and platforms you live in daily (email, calendar, CRM, design, code…)?
11. Languages you speak/write, and your preferred output language?
12. Your usual working hours / when you're active?
13. Recurring tasks (weekly/monthly) Claude could help with?
14. Hard do's and don'ts (e.g. never send anything without approval)?
15. How do you like decisions framed — one recommendation, or options?
16. Reading preferences — how plain should the English be?
17. Personal projects or side hustles Claude should know about?
18. A short professional bio / background?
19. Goals for the next 6–12 months Claude can help with?
20. Privacy boundaries — anything Claude should never store or share?
21. Devices and OS you use (Mac/Windows/mobile)?
22. Preferred sign-off/name for emails or docs you send?
23. Anything you wish past assistants or tools had understood about you?
24. *(Asked first, not last — see above: their LinkedIn URL, so you can pre-fill most of this.)*



### Company questions (ask at least these ~24)

1. Company name and website?
2. One line: what does the company do?
3. Industry / category?
4. Year founded, stage (startup/growth/enterprise), rough size?
5. Products/services — what does each do?
6. Who is your ideal customer (industry, role, company size, region)?
7. The main problem you solve for them?
8. What makes you different from competitors (positioning)?
9. Top 3–5 competitors?
10. Pricing model (subscription, one-time, tiers)?
11. Brand voice / tone — how should public copy sound?
12. Words/phrases to always use, and ones to never use?
13. Key people / leadership / who's who?
14. Your role and decision authority within the company?
15. Main goals / OKRs / North Star metric this year?
16. Main marketing and sales channels?
17. Tools/stack the company uses (CRM, analytics, ad platforms…)?
18. Common data sources Claude may need — and which is the source of truth?
19. Compliance or legal limits on what can be said publicly?
20. Recurring reports or deliverables the company produces?
21. Customer pain points / objections you hear most?
22. Case studies, testimonials, or proof points?
23. Anything confidential Claude must never put in public-facing copy?
24. *(Asked first, not last — see above: their company website, so you can pre-fill most of this.)*

When each interview ends (or they stop), write the answers into the matching `Memory/` file and tell them what you saved.

---



## STEP 6 — Bring in their existing docs & links

Ask the user to **copy or paste any important documents about themselves or their company** into the right folder:

- Personal docs → `~/Documents/Claude/Context/Personal/`
- Company docs → `~/Documents/Claude/Context/Company/`

Also ask: **"Do you have Notion docs, Google Drive files, links, or anything else you want Claude to know about?"**

- If yes, and it lives in a tool with a connector (Notion, Drive, etc.), note it. **Add a one-line pointer in the global** `~/.claude/CLAUDE.md` telling future sessions to use that source **only when a task needs it** (so it's not loaded every session and wasting tokens).
- For any files they add into the `Company/` or `Personal/` folders, **update that folder's decision-tree** `CLAUDE.md` **matrix** — add a row naming the file and when to read it. That matrix is what keeps future sessions reading only what each task needs.

---



## STEP 6b — Show them where their files are (never skip this)

> 🔴 **Before this step, re-read “How to talk to them” at the top of this file.** You are hundreds of lines past it and drift is the failure mode here.

**The last group finished setup with no idea a `Documents/Claude` folder existed.** Everything you built is invisible to them unless you physically show them. Three things, in this order — and **none of them may stop or delay the setup: if any part fails, note it, tell them the manual version at the end, and keep going.**

### 1. Try to pin the folder where they'll see it every day

**Windows — this works, do it.** Pins `Documents\Claude` to **Quick access** in the File Explorer sidebar:

```powershell
$p = Join-Path $env:USERPROFILE 'Documents\Claude'
(New-Object -ComObject Shell.Application).Namespace($p).Self.InvokeVerb('pintohome')
```

Then confirm it's there. If the command errors on their Windows version, don't fight it — fall back to the instructions in part 3.

**Mac — don't try. Go straight to parts 2 and 3.** The Finder sidebar Favorites list lives in a locked-down system file that isn't safely editable from the command line, there's no AppleScript for it, and the tool that does it properly isn't installed. **Do not install anything to make this work** — part 3 has a two-click instruction the user can do themselves in five seconds, and it's a better outcome anyway because they learn where the folder is.

### 2. Open the folder on their screen — always do this

This is the part that actually lands. Open it so it appears in front of them:

```bash
open ~/Documents/Claude          # Mac
```
```powershell
explorer "$env:USERPROFILE\Documents\Claude"   # Windows
```

Then say, in plain words: **"This window that just opened is your Claude folder. Everything I set up lives here — this is where your files go from now on."**

### 3. Tell them how to pin it themselves — 10 seconds, no jargon

Say this at the very end, after the checklist. Keep it exactly this short:

**Mac:**
> "One last thing so you can always find this again: in the window I just opened, click **File** at the top of the screen, then click **Add to Sidebar**. Now it's always in the list down the left side, one click away."

*(If they can't find it, the drag works too: drag the small folder icon next to the word "Claude" at the top of the window into the list on the left.)*

**Windows:**
> "One last thing so you can always find this: right-click the **Claude** folder and choose **Pin to Quick access**. Now it's always in the left side of any window you open." *(Skip if you already pinned it in part 1 — instead just say: "I've pinned it to the left side of File Explorer for you, so it's always there.")*

**Also tell them the plain path once, out loud:** "It's in your Documents folder, inside a folder called Claude." That single sentence is what they'll actually remember.

---



## STEP 7 — Connect their Gmail, Calendar and Drive (LAST — save this for the end)

> 🔴 **Before this step, re-read “How to talk to them” and the HARD RULE at the top of this file.** You are hundreds of lines past it and drift is the failure mode here.

**Do this after everything else, including the interview.** It's the most technical, most fiddly part of the whole setup, and it's the one most likely to stall. Everything before it has already delivered value, so if this one drags, they've still got a fully working setup.

**Never say "Google Workspace CLI", "GWS", "install the CLI", "OAuth", "API", or "credentials" to them — those words mean nothing to a first-time user.** Ask it like this, in exactly this kind of plain language:

> "Last thing, and it's the most useful one: do you use Gmail? I can connect it so I can read your email, write drafts for you, and check your calendar. It takes a few minutes and it's a bit fiddly — but I'll do all of it, you just click **Allow** when Google asks. Want to?"

If they say yes, follow the instructions in `Setup Files/google-workspace-cli-installer-guide.md` for the address they named.

**While you work through it:**

- **Do the technical work yourself and stay quiet about the mechanics.** The only things they should ever have to do are pick their Google account, click **Allow** on Google's own screen, and tell you when it's done.
- **Warn them once, up front, that it has a few steps** — expectations set early stop them worrying that something's broken.
- **If it fails, don't grind on it in front of them.** Tell them plainly: "This one's being stubborn — everything else is set up and working. We can finish this part another time; just tell me 'connect my Gmail' in a new session." Then finish with STEP 8.

If they say no, or don't use Gmail, skip it and move on. **Don't sell it twice.**

---



## STEP 8 — Verify and report

Run a checklist and report it to the user:

- ✅ Detected OS correctly and used the right paths throughout.
- ✅ **Mac:** `~/Documents` is not hidden (`ls -lO ~ | grep Documents` shows no `hidden` flag), and you settled where Documents really lives if OneDrive or iCloud had moved it.
- ✅ `~/Documents/Claude/` has `CLAUDE.md`, `Context/`, `Memory/`, `Skills/`, `Scheduled/`, `Tasks/`.
- ✅ Every file under `~/Documents/Claude/` was run through `Setup Files/setup-os-paths.py` for the detected OS — no `<!--os:` markers remain anywhere in the tree.
- ✅ `~/.claude/CLAUDE.md` exists and contains the global rules (merged, if they had one).
- ✅ `~/.claude/CLAUDE.md` was **also** run through `setup-os-paths.py` (STEP 2) — searching it for `<!--os:` returns zero hits. This file is outside `~/Documents/Claude/`, so STEP 1b does not cover it.
- ✅ `~/.claude/CLAUDE.md` contains the **"My Knowledge Base"** section pointing at `Memory/personal.md`, `Memory/company.md`, and `Context/` — verified by actually reading the file back, with the paths matching where the knowledge base really lives on this machine.
- ✅ `Skills - Claude Cowork` shortcut exists in `~/Documents/Claude/` and points to the canonical skills folder (or skipped, with reason, if no desktop app).
- ✅ `sync-skills-to-commands.sh` exists, ran once, and wrote a `/skill-name` command into `~/.claude/commands/` for each skill; the SessionStart hook in `~/.claude/settings.json` is wired for startup. **These two are the pass mark.** The optional watcher (STEP 3b part 3) is a bonus — if you skipped it or it didn't take, that is a **pass**, and you should not mention it to the user at all.
- ✅ The seven safety checks are in `~/.claude/hooks/` and wired into `settings.json` (STEP 3c), and you **proved at least one fires** rather than assuming. Any you skipped — Python missing, `jq` missing, Windows — say which and why. **Skipping some is a pass; a silent unwired check is not.**
- ✅ You told them, once, that Claude sometimes answers and then corrects itself, and that this is a check working rather than a glitch.
- ✅ 🔴 **Claude for Chrome is installed AND signed in** — you verified it by actually trying a browser tool, not by taking their word for it (STEP 4). If it isn't working, you told them the one thing to do to finish it.
- ✅ Control Chrome added on Mac, or noted as skipped.
- ✅ Gmail/Calendar connected (STEP 7), or they declined, or it failed — say which, in plain words.
- ✅ 🔴 **You finished the setup.** You didn't get pulled into other work partway through. Anything they asked for mid-setup is saved in `Tasks/` and you've reminded them to start a new session for it.
- ✅ `Memory/personal.md` and `Memory/company.md` are filled in (or have the user's partial answers).
- ✅ Any docs/links the user mentioned are in the right `Context/` folder and referenced in the matching matrix.
- ✅ 🔴 **You opened the `Documents/Claude` folder on their screen and said out loud where it is** (STEP 6b). Pinned to Quick access on Windows, or told them the 10-second drag on Mac. **Never end the setup without doing this** — otherwise everything you built is invisible to them.

If anything is only half-done (e.g. they stopped the interview early, or skipped the browser tools), say so plainly and tell them the next step to finish it. Don't report it as done if it isn't.

**Keep the report short.** Three or four plain sentences about what they can now do — not a walkthrough of the checklist above. That checklist is for you.

---



## STEP 9 — 🔴 End the session. Send them to a NEW one.

> 🔴 **Before this step, re-read the HARD RULE and “Teach as you go” at the top of this file.** You are hundreds of lines past it and drift is the failure mode here.

**This is the last thing you say, and you must not skip it.** The setup is finished — **this session's job is done, and it should not be used for anything else.** Last time, people carried straight on working in the setup session and it went badly: a session loaded with setup history is slower, more distracted, and worse at the actual work than a clean one.

**So don't just tell them it's finished. Tell them to stop and start fresh, and tell them why.** Say it roughly like this — your words, same shape:

> "You're all set — everything's installed and I know who you are now.
>
> **One important thing before you start using me: don't keep working in this window.** Click **New** at the top left to start a fresh session, and do your real work there.
>
> Here's why, and it's the most useful habit you'll pick up today: **one session, one job.** This session is full of setup — file copying, settings, installation. If you ask me to write an email in here, I'm dragging all of that around with me while I do it. A fresh session starts clean and gives you noticeably better answers, faster. Same idea as not having one giant conversation for everything.
>
> Everything I learned about you is saved, so a new session already knows you. You never have to explain yourself again."

**Then, if they asked for anything during the setup, hand it back to them as their first job:**

> "You asked me about **[their request]** earlier — I saved it in your Tasks folder. That's the perfect first thing to try: open a new session and ask me there."

**If they ignore this and ask you to do more work in this session anyway:** don't do it. Say it once more, in one friendly line, and stop.

> "Genuinely, start a new session for that — you'll get a better answer out of me. Click **New** at the top left and paste the same question in."

**Do not do the work. Do not do a small version of it. Do not say "sure, just this one."** Holding this line is the last thing the setup teaches them, and it's the one that keeps paying off.

---

