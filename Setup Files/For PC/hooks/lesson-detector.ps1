# lesson-detector.ps1 — UserPromptSubmit hook (Windows port of lesson-detector.sh)
#
# Detects correction / teaching-moment language in the user's prompt and injects a
# reminder to APPLY the lesson, per the Self-Improvement Loop in ~/.claude/CLAUDE.md.
# Match = emit JSON on stdout; no match = emit nothing and exit 0.
#
# Keep this in step with the Mac version. The pattern and the injected text are the
# same; only the shell differs. PowerShell -match is case-insensitive by default,
# which is what the Mac version gets from `grep -i`.
#
# It applies the rule rather than asking permission, because ~/.claude/CLAUDE.md's own
# Self-Improvement Loop is imperative and has no permission step. The single exception
# is ~/.claude/CLAUDE.md itself, which is never edited without the user's explicit yes.

$ErrorActionPreference = 'Stop'

try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }
    $prompt = ($raw | ConvertFrom-Json).prompt
} catch {
    exit 0
}
if ([string]::IsNullOrWhiteSpace($prompt)) { exit 0 }

$pattern = "you didn'?t|you did not|you forgot|forgot to|that'?s not what|that'?s wrong|" +
           "why did you|i already (said|told)|i told you|" +
           "still (not|wrong|broken|doesn'?t|didn'?t|isn'?t)|check again|look again|" +
           "redo\b|re-do\b|not what i (asked|meant|wanted|said)|" +
           "wrong (date|number|file|folder|path|data|amount|link)|^no[,.] |\bnope\b|" +
           "so this (never|doesn'?t)|never do th|don'?t ever|" +
           "same (mistake|issue|problem|error) (again|twice)|happen(ed|ing|s)? again|" +
           "you keep|every time you|add a (hard )?rule|update the skill so"

if ($prompt -notmatch $pattern) { exit 0 }

$context = @(
  "TEACHING-MOMENT DETECTOR (lesson-detector hook): This prompt looks like a correction, a repeat instruction, or a 'make sure this never happens again' moment. First resolve the user's request. Then, BEFORE ending the turn, run the Self-Improvement Loop and FINISH it in this same turn:"
  "(1) State the generic, reusable lesson in one line, do-this / don't-do-that form, not tied to today's specific case."
  "(2) ARGUE AGAINST IT FIRST, as a third-party outsider who has never seen this repo: will it genuinely help EVERY future session, or is it just this one edge case? Name the measurement that would prove you wrong."
  "(3) VERIFY IT IS TRUE AND NOT ALREADY THERE - re-run the measurement and re-read the target file."
  "(4) DECIDE AND ACT NOW, without asking: holds as written -> apply it; too broad -> narrow it and apply the narrow version; one-off or wrong -> withdraw it and say so."
  "Route it per the routing rules: the active skill's SKILL.md or a reference file (bump the version + add a CHANGELOG row), the project CLAUDE.md, or a Memory MEMORY.md. Then tell the user what you changed and which of the three you chose."
  "DO NOT ask permission first - the Self-Improvement Loop is imperative and the Stop hook check-durable-rule-edits.py expects the edit applied, not proposed."
  "THE ONE EXCEPTION: ~/.claude/CLAUDE.md itself is never edited without the user's explicit written permission - for that file, propose and wait."
  "If on reflection the prompt was not actually a correction (false positive), ignore this reminder entirely - do not mention it."
) -join ' '

@{
  hookSpecificOutput = @{
    hookEventName    = 'UserPromptSubmit'
    additionalContext = $context
  }
} | ConvertTo-Json -Depth 5 -Compress

exit 0
