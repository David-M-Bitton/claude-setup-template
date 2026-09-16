# Reference: Packaging the .skill File

Load this file only when creating or updating the `.skill` zip package.

---

## File Writing Rules by Type

| What you're writing | Correct method |
|---|---|
| `SKILL.md`, `CHANGELOG.md`, `.json`, `.md`, any text file | **Write / Edit file tools** directly to `mnt/skills/<skill-name>/` |
| Binary files — PNG, JPG, fonts, any non-text asset | **Python `shutil.copy2`** via the mounted path |
| The `.skill` zip package | **Python `zipfile`** staged in `/tmp`, then copy to skill folder |

**Why:** The `Write` tool is text-only — it silently corrupts binary files. Bash cannot write to Mac-mounted paths at all. Python's file operations work correctly on both.

---

## Copying Binary Assets (PNG, images, fonts)

```python
import shutil, os
skill_dir = "/sessions/<current-session>/mnt/skills/<skill-name>"
os.makedirs(f"{skill_dir}/assets", exist_ok=True)
shutil.copy2("/source/path/file.png", f"{skill_dir}/assets/file.png")
```

---

## Pre-packaging: Clean Up Temp Files First

Before packaging, scan the skill folder for files that should NOT be in the final zip:
- **Stale temp files** from failed bash zip attempts (e.g. `zifcX2Mt`, `ziffWuh9`, or any random-looking name with no extension)
- **`.DS_Store` files** — macOS automatically creates these in any folder when Finder views it. They get included in the zip and clutter the installed skill. Always exclude them from the zip AND delete them from the source folder.
- **Old `.skill` files** from prior packaging runs (filtered in the zipfile loop, but cleaner to delete the destination first)

```python
import os

skill_dir = "/sessions/<current-session>/mnt/<workspace>/<skill-name>"

# Detect cleanup targets: known junk + temp files
known_exts = ('.md', '.json', '.js', '.skill', '.py', '.txt', '.html', '.css')
known_names = {"SKILL.md", "CHANGELOG.md", "evals", "references", "assets", "scripts", "tests"}
junk_names = {".DS_Store", "Thumbs.db", "._.DS_Store"}
to_delete = []
for f in os.listdir(skill_dir):
    full = os.path.join(skill_dir, f)
    if os.path.isfile(full):
        if f in junk_names:
            to_delete.append(full)
        elif f not in known_names and not any(f.endswith(e) for e in known_exts):
            to_delete.append(full)

for f in to_delete:
    try:
        os.remove(f)
    except PermissionError:
        # Don't ask user. Use the Cowork delete-permission tool, then retry.
        # call allow_cowork_file_delete(file_path=f) here, then:
        os.remove(f)
```

**`.DS_Store` PermissionError gotcha:** `.DS_Store` files often resist `os.remove()` with "Operation not permitted" because the source mount restricts deletes. When this happens, call `allow_cowork_file_delete` with the file path (this enables deletes for the whole folder), then retry. **Never ask the user to delete files manually.**

**In the zipfile loop**, also explicitly skip `.DS_Store` even after the cleanup pass — belt and suspenders, since macOS regenerates them quickly:

```python
for file in files:
    if file.endswith('.skill') or file == '.DS_Store':
        continue
    ...
```

---

## Packaging the .skill File

Always use Python zipfile. Never use bash zip into the mount (fails mid-write on network mounts, leaves stale temp files like `zifcX2Mt`).

```python
import shutil, os, zipfile

skill_dir = "/sessions/<current-session>/mnt/skills/<skill-name>"
tmp_zip = "/tmp/<skill-name>.skill"
dest = f"{skill_dir}/<skill-name>.skill"

if os.path.exists(dest):
    os.remove(dest)

with zipfile.ZipFile(tmp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.skill'):
                continue  # NEVER remove this filter — prevents stale .skill inside zip
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, skill_dir)
            zf.write(full_path, arcname)

shutil.copy2(tmp_zip, dest)
os.remove(tmp_zip)
```

The `.skill` zip must have `SKILL.md` at the **root level** (not nested in a subfolder). The installer validates this and will reject the file with "Zip must contain a SKILL.md file" if it's missing or nested.

---

## Validation — Run Before present_files

After creating the `.skill` file, run these checks. If any fail, fix and repackage.

```python
import zipfile

skill_path = "/tmp/<skill-name>.skill"
with zipfile.ZipFile(skill_path, 'r') as zf:
    names = zf.namelist()

# Check 1: SKILL.md must be at root level (not nested)
skill_md_entries = [n for n in names if n == "SKILL.md" or n.endswith("/SKILL.md")]
root_skill_md = [n for n in skill_md_entries if "/" not in n]
assert root_skill_md, f"FAIL: SKILL.md not at root level. Found: {skill_md_entries}"

# Check 2: Exactly one SKILL.md in the zip
assert len(skill_md_entries) == 1, f"FAIL: Expected 1 SKILL.md, found {len(skill_md_entries)}: {skill_md_entries}"

print(f"✅ Packaging valid. Entries: {names}")
```

**The three errors this prevents:**
1. `SKILL.md file must be in the top-level folder, not nested deeper` — caused by zipping the parent folder instead of the skill folder's contents
2. `Zip must contain exactly one SKILL.md file` — caused by a stale `.skill` file inside the skill folder being included in a new zip
3. `[INVALID_PATH] Failed to resolve path` — caused by presenting from `mnt/skills/` instead of the session working directory

---

## Presenting the .skill File — Default to `computer://`

> ⚠️ **REALITY CHECK (verified across multiple sessions, May 2026):** `present_files` consistently fails with "not accessible on the user's computer" when called on `.skill` files in this user's environment, regardless of path (workspace root, outputs folder, with or without `chmod 644`). Until that's fixed at the Cowork tool level, **skip `present_files` entirely** and use `computer://` markdown links. Trying `present_files` first wastes 2+ tool calls every session.

### The default flow

1. **Copy the `.skill` to BOTH the workspace root AND the outputs folder** on disk. Workspace copy is a silent backup that persists after the session; outputs is the link you'll surface to the user.
   ```python
   shutil.copy2(tmp_zip, f"/sessions/<session>/mnt/<workspace>/<skill-name>.skill")
   shutil.copy2(tmp_zip, f"/sessions/<session>/mnt/outputs/<skill-name>.skill")
   ```
2. **chmod 644 both copies.** Even though we're not using `present_files`, restrictive perms can still block the user from opening the file via `computer://`.
3. **Drop ONE `computer://` markdown link in the chat reply** — pointing at the outputs folder. **Do not surface the workspace backup unless the user reports the primary link is broken.** Two links for one skill confuses users (verified: a user asked "why are you presenting 2 skills to save?" — the dual-link pattern read as two skills, not one + backup).
   ```markdown
   [Install <skill-name>](computer:///<mac-outputs-path>/<skill-name>.skill)
   ```
4. **Tell the user what to do, briefly:** "Click → Finder opens → double-click the `.skill` to install."

### When to try `present_files` (rarely)

Only try `present_files` if:
- The user explicitly asks for a one-click install card, AND
- You've never tried it in this session before

If you do try it: ONE attempt, workspace root path, with `chmod 644`. If it fails, immediately fall back to `computer://`. **Do NOT try a second path.** Do NOT try outputs folder. Do NOT retry after chmod. Two empirical sessions = two failures across all paths = stop.

### Hard rules

- **Default to `computer://` links.** Don't reach for `present_files` first.
- **Surface ONE `computer://` link in chat** — outputs folder. Save a workspace backup silently on disk; only surface the backup link if the user reports the primary doesn't work.
- **chmod 644 every `.skill` file you create** so the user can open it from Finder regardless of which install path they use.
- **Never** use the `mnt/skills/` path or `mnt/.claude/skills/...` for any install link — these are sandbox/read-only and won't resolve.
- **If a future Cowork update fixes `present_files`,** revert this section to the older "Use the Fallback Ladder" pattern. Until then, `computer://`-first is the documented working flow.

### Why each path fails (for debugging)

| Path | Behavior observed | Why |
|---|---|---|
| Workspace ROOT (Mac path) | `present_files` rejects with "not accessible" | Unknown — Cowork tool-level issue. Mac path resolves correctly via `computer://` though. |
| Outputs folder (Mac path) | Same rejection | Same issue. `computer://` link to this path works. |
| Subfolder inside workspace | Same rejection | `present_files` may scope to specific roots only. |
| `mnt/skills/<skill-name>/<file>.skill` | `[INVALID_PATH]` | Sandbox-only path; not on the user's Mac. |
| `mnt/.claude/skills/...` | `[INVALID_PATH]` | Read-only mount; not on the user's Mac. |

If you find `present_files` working again, log it in the skill's CHANGELOG and update this section to revert to the ladder approach.
