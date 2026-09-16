#!/bin/bash
# lesson-detector — UserPromptSubmit hook
# Detects correction / teaching-moment language in the user's prompt and injects a
# reminder to APPLY the lesson (per the Self-Improvement Loop in ~/.claude/CLAUDE.md).
# Match = inject; no match = silent.
#
# 🔴 REWRITTEN 2026-09-03. It used to end with "ask the user: 'Want me to save this
# rule there?' ... do NOT write the rule without their yes." That contradicted
# ~/.claude/CLAUDE.md's own Self-Improvement Loop, which is imperative and has no
# permission step: "After ANY correction, update the skill being worked on ... Bump the
# skill's version + add a CHANGELOG.md entry. Tell the user in the session what you
# updated." It also contradicted the Stop hook check-durable-rule-edits.py, added the
# same day on the user's instruction that a rule which passes the every-session test "can
# automatically apply now". Apply and report; do not ask.
#
# ⛔ ONE CARVE-OUT SURVIVES: ~/.claude/CLAUDE.md itself. Its first line is "Never edit
# this file without the user's explicit written permission", and the Self-Improvement Loop
# is explicitly scoped "(targets the active skill — NOT this global file)".
#
# ⚠️ THIS HOOK DOES NOT REPLACE THE TWO Stop HOOKS, and must not be sold as doing so.
# It fires only on a correction-shaped USER PROMPT. Measured 2026-09-03: of five real
# prompts in one session that produced rule writes, FOUR were silent here — a rule far
# more often comes from the user asking for one directly than from him correcting a
# mistake. check-deferred-learnings.py and check-durable-rule-edits.py fire on what
# CLAUDE does, which is the common path. This one front-loads the argument so those two
# find it already done and stay silent; that is the whole of the overlap.

prompt=$(jq -r '.prompt // empty' 2>/dev/null)
[ -z "$prompt" ] && exit 0

pat="you didn'?t|you did not|you forgot|forgot to|that'?s not what|that'?s wrong|why did you|i already (said|told)|i told you|still (not|wrong|broken|doesn'?t|didn'?t|isn'?t)|check again|look again|redo\b|re-do\b|not what i (asked|meant|wanted|said)|wrong (date|number|file|folder|path|data|amount|link)|^no[,.] |\bnope\b|so this (never|doesn'?t)|never do th|don'?t ever|same (mistake|issue|problem|error) (again|twice)|happen(ed|ing|s)? again|you keep|every time you|add a (hard )?rule|update the skill so"

if printf '%s' "$prompt" | grep -qiE "$pat"; then
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"TEACHING-MOMENT DETECTOR (lesson-detector hook): This prompt looks like a correction, a repeat instruction, or a 'make sure this never happens again' moment. First resolve the user's request. Then, BEFORE ending the turn, run the Self-Improvement Loop and FINISH it in this same turn: (1) State the generic, reusable lesson in one line, do-this / don't-do-that form, not tied to today's specific case. (2) ARGUE AGAINST IT FIRST, as a third-party outsider who has never seen this repo: will it genuinely help EVERY future session, or is it just this one edge case? Name the measurement that would prove you wrong. (3) VERIFY IT IS TRUE AND NOT ALREADY THERE - re-run the measurement and re-read the target file. Measured 2026-09-03: of two lessons about to be saved, one was a misdiagnosis and the other was already in the target file. Neither survived. (4) DECIDE AND ACT NOW, without asking: holds as written -> apply it; too broad -> narrow it and apply the narrow version; one-off or wrong -> withdraw it and say so. Route it per the routing rules: the active skill's SKILL.md or a reference file (bump the version + add a CHANGELOG row), the project CLAUDE.md, or a Memory MEMORY.md. Then tell the user what you changed and which of the three you chose. DO NOT ask permission first - ~/.claude/CLAUDE.md's Self-Improvement Loop is imperative and the Stop hook check-durable-rule-edits.py expects the edit applied, not proposed. THE ONE EXCEPTION: ~/.claude/CLAUDE.md itself is never edited without the user's explicit written permission - for that file, propose and wait. If on reflection the prompt was not actually a correction (false positive), ignore this reminder entirely - do not mention it."}}
JSON
fi
exit 0
