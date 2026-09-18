# Getting Remote Control back on Claude Code Desktop routines

Claude Code Desktop can run **routines** — scheduled tasks that fire on their own, overnight,
with nobody watching. Remote Control is the feature that makes a session openable from your
phone or from claude.ai/code.

Since a Desktop update in early September 2026, routines stopped getting Remote Control. They
run, they work, and you cannot open a single one of them from your phone.

This repo has two working ways around that, and the measurements behind both.

---

## The regression

Tracked upstream as [anthropics/claude-code#92276](https://github.com/anthropics/claude-code/issues/92276),
open since **2026-09-05**:

> Desktop 1.44121.4+ never auto-enables Remote Control for scheduled-task sessions (regression from 1.40609.0)

Desktop `1.40609.0` bridged scheduled tasks fine. `1.44121.4` does not, and neither does any
build since. Nothing in the user's settings changed.

The cause is one added term in the app's own policy check. In `app.asar`:

```js
shouldEvaluateRemoteControlPolicy(e){
  return (this.remoteControlPolicyCovers(e) || !!e.remoteControlUserRequested)
      && !e.remoteControlEnabled && !e.remoteControlUserToggled && !e.remoteControlAutoInFlight
}
remoteControlPolicyCovers(e){ return !!e.remoteControlAutoEligible && !e.scheduledTaskId }
```

`&& !e.scheduledTaskId` is the whole regression. Builds before the change do not contain
`remoteControlPolicyCovers` at all.

**The important half is the part people miss:** `scheduledTaskId` only blocks the *automatic*
path. The door is not locked — nothing is pushing it. That is what both workarounds exploit.

### What does NOT fix it

Measured on real scheduled runs, not guessed:

| Attempt | Result |
|---|---|
| `remoteControlAtStartup: true` in settings | No effect. The scheduled run returns from `maybeAutoEnableRemoteControl` **before** the settings resolver is ever consulted. |
| `ccRemoteControlDefaultEnabled: true` | Already on. The gate is downstream of it. |
| `remoteTools.allowUnattendedServing` | Unrelated — governs a cloud session running commands on your machine. |
| `set_remote_control` called **by** a routine | Refused. The check is on the CALLER, and the target id never enters it. Tested against three targets, byte-identical refusal each time. |
| `claude remote-control --session-id <local id>` | `--session-id` means a *remote* session id, not a Desktop local one. |
| Patching `app.asar` | Breaks the macOS code signature (hardened runtime) and every update silently reverts it. Don't. |

---

## Workaround 1 — the helper session (works with the screen LOCKED)

**This is the one to use.** See [`helper-session-prompt.md`](helper-session-prompt.md).

One normal session, left open, arms its own in-session timer. Every 5 minutes through the
routine window it finds running routines and turns Remote Control on for each.

Why it works with the Mac locked: the tool's attendance check reads only `scheduledTaskId` and
dispatch ancestry. **It never looks at screen lock, keyboard, or window focus.** A normal
session's own timer is a perfectly valid attended caller at 5am on a locked machine.

**Proven twice, screen lock verified programmatically both times** (`CGSSessionScreenIsLocked = Yes`),
on two different routines, each a fresh run started while locked:

| | Trial 1 | Trial 2 |
|---|---|---|
| `bridgeSessionIds` | populated | populated |
| `remoteControlUserEnabled` | `true` | `true` |
| `scheduledRunContinued` | unset — still a routine | unset |
| Permission card | none | none |

🔴 **One hard precondition: the routine must still be RUNNING.** A finished, stopped run is
refused with *"Remote Control requires an active session. Send a message first."* That is why
the helper sweeps on a timer instead of tidying up afterwards. The bridge itself does persist
after the run ends, so the link still works later.

---

## Workaround 2 — type the command (needs the screen UNLOCKED)

[`rc-bridge.sh`](rc-bridge.sh). Focuses a session with the app's own `claude://` deep link,
checks Claude is frontmost, types `/remote-control`, presses Return twice, then polls the
session record for a bridge id.

```bash
./rc-bridge.sh                      # bridges the current session
./rc-bridge.sh local_abc123...      # bridges a specific one
```

Two details that cost real time to find:

- **Return twice.** The first Return is eaten by the slash-command autocomplete popup as
  "accept the highlighted item". The second one sends.
- **Poll long.** The app persists this state asynchronously and can take well over a minute. A
  30-second poll reported a false failure on a run that had actually worked.

**Use this when you are at the machine.** Key events are not delivered while the screen is
locked, so it cannot cover overnight routines — the script refuses to type rather than firing
blind into whatever window you left open.

---

## Reading the result correctly

Everything here is judged on one field in the session record at
`~/Library/Application Support/Claude/claude-code-sessions/<a>/<b>/<sessionId>.json`:

- ✅ **`bridgeSessionIds`** — a list with an id in it means Remote Control is on. This is the
  only field that decides. Not an exit code, not a tool returning without error.
- ⚠️ **`remoteControlAutoEligible`** flips `true` → `false` **on success**. It means "no longer
  a candidate", because it is now on. Reading `false` as failure inverts the answer.
- ⚠️ **`remoteControlEnabled`** is never written at all, on or off. It tells you nothing.
- ✅ **`remoteControlUserEnabled`** going absent → `true` is a genuine second success signal.

And the link's shape is itself the signal: `claude://claude.ai/epitaxy/...` is a local deep
link meaning **off**. `https://claude.ai/code/...` means **on** and opens on any device.

---

## Limits, stated plainly

- The helper's timer is session-only, dies with the session or the app, and recurring timers
  expire after 7 days.
- Timers fire only while the helper session is idle.
- Survival across system sleep and app restart is **untested**.
- None of this is a supported API. It is a workaround for an open bug, and a fix upstream
  should replace it.

---

*Measured on macOS, Claude Code Desktop 2.110.1, 2026-09-18.*
