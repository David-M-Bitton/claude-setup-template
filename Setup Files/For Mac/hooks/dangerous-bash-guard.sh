#!/usr/bin/env bash
# PreToolUse guard on Bash. MERGED 2026-08-07 from three sources, all kept:
#   1. dangerous-bash-guard  (this playbook, 30-hooks-and-automation.md §3)
#      -> ref RESOLUTION instead of substring matching, + non-git danger
#         (rm -rf /, curl|bash, destructive SQL in execution shape).
#         Verified against 17 cases 2026-08-04.
#   2. mattpocock-skills:git-guardrails-claude-code
#      -> the LOCAL destructive git ops nothing else here covered:
#         reset --hard, clean -f/-fd, branch -D, checkout ., restore .
#   3. the no-mistakes gate (70-code-review-and-prs.md §1-0-ii)
#      -> one allowlisted push target, and it becomes MANDATORY once the
#         gate remote actually exists in this repo.
#
# Why merged and not two hooks: two PreToolUse/Bash hooks both policing git
# drift apart silently. One owner per concern. See 30 §2a.
set -euo pipefail

input="$(cat)"
command="$(echo "$input" | jq -r '.tool_input.command // empty')"
[ -z "$command" ] && exit 0

# Normalise before matching: collapse whitespace runs, and strip the arg forms
# that let a push hide from a naive pattern. `git -C <path> push` is the one
# that matters here -- -C is how you drive a worktree, and worktree-per-task
# is this project's build model (35-subagents-and-orchestration.md §4).
norm="$(echo "$command" | tr -s '[:space:]' ' ' | sed -E 's/(^| )git +(-C +[^ ]+|--no-pager|--git-dir=[^ ]+|--work-tree=[^ ]+) +/\1git /g')"

# NARROWED 2026-08-27. Was '([^[:space:]]+[[:space:]]+)*' between git and push,
# which allowed ANY tokens in the gap. Two false positives in one session:
#   `git stash push -- <path>`  -- not a network push at all, blocked anyway.
#   `no-mistakes axi run --intent "...git checkout... the push step..."` -- no
#   git command present; the gap matched across unrelated PROSE in an argument.
# The gap only ever needs to hold git's GLOBAL options, and those all start with
# `-`. Requiring that is what separates an option from a subcommand (`stash`) or
# from an English word. Options taking a separate value get their value too, so
# `git -C /path push` and `git -c a=b push` still match. Line 26's sed already
# strips the four commonest of these, so this is the second line of defence.
is_push='(^|[[:space:];&|(])git[[:space:]]+(((-[Cc]|--git-dir|--work-tree|--namespace|--exec-path)[[:space:]]+[^[:space:]]+|-[^[:space:]]*)[[:space:]]+)*push([[:space:]]|$)'

# --- ALLOWLIST: the verification gate is the one permitted push target. ---
if echo "$norm" | grep -Eq '(^|[[:space:];&|(])git[[:space:]]+push[[:space:]]+no-mistakes([[:space:]]|$)'; then
  exit 0
fi

if echo "$norm" | grep -Eq "$is_push"; then
  current_branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"

  # (a) Never push from main/master, whatever the spelling. Resolving the ref
  #     is the point: a substring match on `git push origin main` misses
  #     `git push origin HEAD`, which pushes to main when main is checked out.
  case "$current_branch" in
    main|master)
      echo "Blocked: you are on '${current_branch}' and this is a git push. Open a branch and a PR (70-code-review-and-prs.md §1a). Every spelling is blocked, including 'git push origin HEAD'." >&2
      exit 2
      ;;
  esac

  # (b) If this repo has a no-mistakes gate, the gate is the ONLY way out.
  #     Before `no-mistakes init` there is no gate, so ordinary feature-branch
  #     pushes still work -- this tightens itself the moment the gate exists
  #     rather than blocking work that has nowhere else to go.
  if git remote 2>/dev/null | grep -qx 'no-mistakes'; then
    echo "Blocked: this repo has a no-mistakes gate, so every push goes through it. Use: git push no-mistakes" >&2
    exit 2
  fi
fi

deny_patterns=(
  # --- from the playbook's own guard ---
  # NARROWED 2026-08-07. Was 'rm[[:space:]]+-rf[[:space:]]+/', which matched
  # the leading slash of ANY absolute path -- `rm -rf /tmp/scratch` was
  # blocked. Caught in live use. The intent is root and root-glob only, so
  # the slash must be the whole argument or immediately followed by a glob.
  # `rm -rf ~` and `rm -rf $HOME` are covered by the two rules after it.
  'rm[[:space:]]+-rf[[:space:]]+/([[:space:]]|$|\*)'
  'rm[[:space:]]+-rf[[:space:]]+~([[:space:]]|/|$)'
  'rm[[:space:]]+-rf[[:space:]]+\$(HOME|\{HOME\})'
  'git[[:space:]]+push[[:space:]]+--force'
  'push[[:space:]]+--force'
  'curl[^|]*\|[[:space:]]*(ba)?sh'
  'wget[^|]*\|[[:space:]]*(ba)?sh'
  # Match the EXECUTION SHAPE, not the substring. A bare `DROP TABLE` match
  # also blocked `manage.py sqlmigrate`, the migration-review path a
  # non-coder needs (55-data-and-backend.md §6). → dry-run finding 19.
  '(psql|dbshell|mysql)([^;&|]*)(DROP[[:space:]]+(TABLE|DATABASE)|TRUNCATE)'
  '[[:space:]]-c[[:space:]].{0,200}(DROP[[:space:]]+(TABLE|DATABASE)|TRUNCATE[[:space:]]+TABLE)'
  '(DROP[[:space:]]+DATABASE|DROP[[:space:]]+SCHEMA[[:space:]]+public)'
  # --- from Matt Pocock's git-guardrails: LOCAL destructive git ---
  # These destroy uncommitted work. Nothing else in this playbook covered them.
  'git[[:space:]]+reset[[:space:]]+--hard'
  'git[[:space:]]+clean[[:space:]]+-[a-z]*f'
  'git[[:space:]]+checkout[[:space:]]+\.([[:space:]]|$)'
  'git[[:space:]]+restore[[:space:]]+\.([[:space:]]|$)'
)

# --- case-SENSITIVE rules -----------------------------------------------
# These run outside the loop below, which greps with -i and so cannot tell an
# uppercase flag from a lowercase one.
#
# `git branch -D` force-deletes a branch whose commits may exist nowhere else.
# `git branch -d` REFUSES unless the work is already merged, so it cannot lose
# anything. It is the safe flag and the one to reach for.
#
# SPLIT 2026-08-29 on the user's instruction. One case-insensitive rule blocked
# BOTH forms, so the guard's own advice ("use the safe form") was itself
# blocked and routine cleanup of merged branches had to be done by hand.
# The force flag stays blocked: deleting unmerged local work is unrecoverable.
# It is not on a remote, not in a PR, and not findable in Dropbox history.
# --- CARVE-OUT 2026-08-31 on the user's instruction: the agent may delete a branch
#     whose work is PROVABLY already in the remote's history. -----------------
#
# Why: `-d` refuses a squash-merged branch, because squashing means the branch
# tip is never an ancestor of main. So the two safe-looking options both failed
# and routine cleanup could only be done by hand. Measured on a ticket: two
# branches, both merged (PR #62, #64), both un-deletable by the agent.
#
# ⛔ This does NOT loosen the rule. The rule was "never lose unmerged work", and
# that is exactly what is still enforced -- just measured properly instead of
# approximated by "is the tip an ancestor". A branch is deletable only if it is
# PROVED redundant, by one of two independent tests, and anything unproved is
# blocked. Every failure path blocks: a missing ref, an unparseable command, an
# absent remote, `gh` being offline, a git error. There is no path where doubt
# means allow.
branch_delete_is_safe() {
  local cmd="$1"

  # (1) SHAPE. Only the bare form, and nothing else on the line. No `cd x &&`,
  #     no `git -C`, no chaining, no substitution, no globs. This is not
  #     fussiness: the hook resolves branches in ITS OWN cwd, so a command that
  #     could change directory or target another repo would be checked against
  #     the wrong history. Line 26's sed strips `-C <path>`, which is precisely
  #     how that would go unnoticed.
  case "$cmd" in
    *';'*|*'&'*|*'|'*|*'$('*|*'`'*|*'>'*|*'<'*|*'*'*|*'?'*|*'['*|*'--'*) return 1 ;;
  esac
  # Exactly: git branch -D name [name...]   (leading/trailing space tolerated)
  if ! echo "$cmd" | grep -Eq -- '^[[:space:]]*git[[:space:]]+branch[[:space:]]+-D([[:space:]]+[A-Za-z0-9._/-]+)+[[:space:]]*$'; then
    return 1
  fi

  # (2) The comparison point: the remote's default branch. No remote, no proof.
  local upstream
  upstream="$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null || true)"
  [ -z "$upstream" ] && upstream="refs/remotes/origin/main"
  git rev-parse --verify --quiet "$upstream" >/dev/null 2>&1 || return 1
  local upstream_tree
  upstream_tree="$(git rev-parse --verify --quiet "${upstream}^{tree}" 2>/dev/null || true)"
  [ -z "$upstream_tree" ] && return 1

  local repo_slug
  repo_slug="$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || true)"

  local head_branch
  head_branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"

  local name
  for name in $(echo "$cmd" | sed -E 's/^[[:space:]]*git[[:space:]]+branch[[:space:]]+-D[[:space:]]+//'); do
    # Never the branch you are on, and never a default-branch name however spelled.
    case "$name" in
      main|master|develop|"$head_branch") return 1 ;;
    esac

    local tip
    tip="$(git rev-parse --verify --quiet "refs/heads/${name}" 2>/dev/null || true)"
    [ -z "$tip" ] && return 1

    # TEST A (offline): merging it into the default branch would change nothing,
    # so it holds nothing the default branch lacks. Catches the ordinary case and
    # needs no network. A conflict makes merge-tree print a different tree or
    # fail -- either way this test simply does not pass, and B is tried.
    local merged_tree
    merged_tree="$(git merge-tree --write-tree "$upstream" "$tip" 2>/dev/null || true)"
    if [ -n "$merged_tree" ] && [ "$merged_tree" = "$upstream_tree" ]; then
      continue
    fi

    # TEST B (authoritative): GitHub says a PR whose head was THIS branch is
    # merged, and the local tip is contained in what that PR carried. The second
    # half is the one that matters -- a merged PR alone would happily authorise
    # deleting commits added locally AFTER the merge.
    #
    # ⚠️ Needed because TEST A fails on exactly the branch this carve-out exists
    # for: once main moves on, an older branch touching the same lines conflicts.
    [ -z "$repo_slug" ] && return 1
    local pr_num pr_head
    pr_num="$(gh pr list --repo "$repo_slug" --head "$name" --state merged \
                --json number --jq '.[0].number // empty' 2>/dev/null || true)"
    pr_head="$(gh pr list --repo "$repo_slug" --head "$name" --state merged \
                 --json headRefOid --jq '.[0].headRefOid // empty' 2>/dev/null || true)"
    [ -z "$pr_head" ] && return 1

    # 🔴 FETCH THE EVIDENCE, DO NOT LOWER THE BAR. Added 2026-09-01.
    #
    # The gate pushes its own fix commits and the remote branch is deleted at
    # merge, so the PR's head commit is often absent from the local object store
    # and the ancestor test below could not run at all. Three of four stale
    # branches failed here for MISSING EVIDENCE, not for cause.
    #
    # ⛔ The tempting fix was to accept "the PR's merge commit is in main" and
    # drop the ancestor test. That is strictly weaker: the ancestor test is the
    # only thing separating "the gate rewrote my branch head" from "someone
    # committed locally and never pushed it", and both look identical otherwise.
    # ⚠️ Measured 2026-09-01: that weakening would have deleted
    # `fix/apify-run-endpoint`, whose local-only commit was the ONLY copy of the
    # a ticket escape-decoding fix -- no remote, and Dropbox does not sync the repo.
    #
    # So retrieve `refs/pull/<n>/head` instead and run the SAME test. Nothing is
    # accepted that was not proved; only the proof becomes reachable. A failed
    # fetch (offline, no such ref) leaves the object absent and still blocks.
    if ! git cat-file -e "$pr_head" 2>/dev/null && [ -n "$pr_num" ]; then
      git fetch --quiet origin "refs/pull/${pr_num}/head" 2>/dev/null || true
    fi

    git rev-parse --verify --quiet "$pr_head" >/dev/null 2>&1 || return 1

    # B-i: the tip is literally contained in what the PR carried. The ordinary
    # case, and the cheapest.
    git merge-base --is-ancestor "$tip" "$pr_head" 2>/dev/null && continue

    # TEST C (content, not ancestry). Added 2026-09-02 on the user's instruction,
    # after the fifth blocked cleanup in a row.
    #
    # 🔴 THE CAUSE TEST B CANNOT SEE: the no-mistakes gate REBASES the commit it
    # was given before pushing it. The work reaches the PR, but as a new commit
    # with a new sha, so the local tip is not an ancestor of anything and never
    # will be. Measured on a branch: submitted e08ff17, gate pushed
    # 3ec84f2, PR #140 merged. Nothing was unmerged; the evidence was simply the
    # wrong shape.
    #
    # ⛔ This is NOT the weakening the block above rejects. That one proposed
    # dropping the containment test entirely and trusting the merged PR, which
    # cannot tell a rebased commit from one committed locally and never pushed.
    # This still proves containment -- by PATCH rather than by sha. `git cherry`
    # prints + for a commit with no equivalent patch upstream, and a local-only
    # commit is exactly that, so it still blocks.
    #
    # ⚠️ Verified against all ten local branches before shipping: it unblocked
    # the four with merged PRs and rebased tips, and STILL blocked a branch
    # and a branch, whose merged PRs sit alongside local commits that
    # have no upstream equivalent -- the fix/apify-run-endpoint case the comment
    # above was written for. A test that said yes to those two would be the
    # weakening, and this one does not.
    [ -z "$(git cherry "$pr_head" "$name" 2>/dev/null | grep '^+' || true)" ] || return 1
  done

  return 0
}

if echo "$norm" | grep -Eq -- 'git[[:space:]]+branch[[:space:]]+(-[a-zA-Z]*D|--delete[[:space:]]+--force|--force[[:space:]]+--delete)'; then
  if branch_delete_is_safe "$command"; then
    exit 0
  fi
  echo "Blocked by dangerous-bash-guard: force-deleting a branch can lose commits that exist nowhere else, and this one is not provably redundant. Use 'git branch -d', which refuses anything unmerged. The agent may use the force form only as 'git branch -D <name>' (no cd, no chaining, no -C) and only for a branch that either merges into origin's default branch as a no-op, or has a MERGED PR on GitHub whose head contains the local tip. If neither holds, run the force form yourself outside Claude Code." >&2
  exit 2
fi

for pattern in "${deny_patterns[@]}"; do
  # `--` is load-bearing: without it a pattern starting with `-` is parsed as
  # a grep OPTION, grep errors, and the `if` reads that as "no match" -- a
  # silently disabled deny rule. Hit exactly this on 2026-08-04.
  if echo "$norm" | grep -Eqi -- "$pattern"; then
    echo "Blocked by dangerous-bash-guard: command matches '${pattern}'. If this is genuinely required, run it yourself outside Claude Code, not through the agent." >&2
    exit 2
  fi
done

exit 0
