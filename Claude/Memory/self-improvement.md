# Self-Improvement Loop (targets the active skill — NOT the global CLAUDE.md)

- After ANY correction from the user, update the skill being worked on. Do NOT update the global `~/.claude/CLAUDE.md` unless the correction applies to every Claude Code session across every project.
- Where the correction goes inside the skill:
  - Behavior rule → add to `SKILL.md` or the skill's own `CLAUDE.md`
  - Detailed context, examples, or workflows → reference file inside `skill/references/`
  - Recurring mistake → add a test to `skill/tests/evals.json` so it's caught next time
  - Always: bump the skill's version line and add a `CHANGELOG.md` entry describing the fix
- Be detailed and specific. "Don't write supplement doses in mg when the lab reports mcg" beats "be careful with units."
- Phrase rules as do-this / don't-do-that, not soft guidance.
- Make the rule generic enough to catch every variant of the mistake, not just today's case.
- Review the skill's `SKILL.md`, `CLAUDE.md`, and relevant reference files at session start before starting work on it.
- If you make the same mistake twice, the rule wasn't strong enough — strengthen it.
