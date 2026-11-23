---
name: cross-agent-code-review
description: >-
  Use this skill whenever a coding agent is asked to implement, modify, fix,
  refactor, or otherwise change code and the user wants another coding agent to
  review the result, exchange findings, clarify disagreements, or iterate until
  agreement. It is provider-neutral and applies when the implementer or
  reviewer is Codex, Claude Code/Desktop, Antigravity, WorkBuddy, Cursor, or
  another agent. The implementing agent owns all edits; the reviewing agent is
  read-only; messages are routed through Agent HUD/MCP or an equivalent bridge
  to the matching project session; continue only for unresolved findings and
  stop at agreement or a bounded escalation.
---

# Cross-agent code review

Use this workflow when one agent changes code and another agent reviews that
change. The names of the products do not matter: treat the agent that edits
the repository as the **implementer** and the other agent as the **reviewer**.

The implementer remains the only agent allowed to edit files. The reviewer
reads the same checkout, reports findings, and may explain or defend a finding
but does not edit, commit, push, or approve destructive actions. This ownership
rule keeps the review loop understandable and prevents two agents from
silently overwriting one another.

## Establish the workflow

A message bridge is required for automatic handoff. Use Agent HUD/MCP or an equivalent bridge that can discover the target session and deliver a message. If no bridge is available, complete the implementation and tests, report that the handoff was not performed, and provide the exact review request for manual delivery.

Before changing code, resolve these values from the user's request and the
available sessions:

- `implementer`: the current agent, unless the user explicitly assigns the
  implementation to another agent.
- `reviewer`: the named target agent. Do not guess a reviewer when the user did
  not identify one and several candidates are available.
- `project`: the actual local project directory or worktree being changed.
- `review_scope`: the feature, files, tests, and behavior the user asked for.
- `max_rounds`: 5 by default. Use a user-specified limit when present.

If the reviewer is specified by product but not by session, use the messaging
bridge's session listing to find a reviewer session whose project directory
matches `project`. If no matching session exists, say so and stop the review
handoff; do not send the request to another project and do not start a new
session unless the user explicitly asked for that.

Both agents should use the same actual checkout for this workflow. A separate
Git worktree is valid only when the user deliberately asks for it and the
reviewer is pointed at the worktree containing the implementer's changes.

## Implement before review

1. Restate the requested behavior briefly and identify the files or subsystem
   that will be affected.
2. Inspect the repository's local instructions and existing tests before
   editing.
3. Implement the change as the implementer.
4. Run the relevant tests, checks, or build commands before requesting review.
5. Inspect `git status --short`, `git diff`, and `git diff --cached`. Include
   untracked files in the review scope; a diff command alone does not show
   them.

Do not commit or push unless the user explicitly requests it. A review can
   examine staged and unstaged changes directly. Do not ask the reviewer to
   reconstruct a change from a pasted full diff when it can read the shared
   checkout; send a compact description, paths, test results, and the review
   scope instead.

## Send the first review request

Use the bridge's session-discovery operation (for example `list_sessions`) and
then its message operation (for example `send_message`). Send one complete
request rather than several fragments:

```text
You are the read-only reviewer for the current project.

Review the implementer's current uncommitted change for: <review_scope>.
Inspect git status, git diff, git diff --cached, and any untracked files that
belong to this change. Read the relevant source and tests yourself.

Do not modify files, commit, push, or approve a destructive action. Report
findings as F1, F2, ... with severity (blocker, high, medium, low), file and
line, evidence, why it matters, and a concrete recommendation. Separate real
defects from optional improvements. If no blocking or actionable findings
remain, end with APPROVED.

Return the review to the implementer through the same messaging bridge.
```

The message must identify the project and the exact review scope, but must not
include credentials, private tokens, or unrelated project content. The bridge
should deliver it to the selected reviewer session, not to every session.

## Evaluate the review

When the reviewer replies, classify every finding before acting:

- **ACCEPTED**: the implementer agrees the finding is valid and will fix it.
- **REJECTED**: the implementer disagrees and can give a technical reason.
- **NEEDS_CLARIFICATION**: the finding or its expected behavior is ambiguous.
- **OUT_OF_SCOPE**: the finding is valid but unrelated to the requested
  change; record it separately rather than silently expanding scope.

Keep the finding IDs stable across rounds. Do not accept a finding merely
because it sounds plausible; inspect the code, tests, contracts, and user
requirements. Do not reject a finding without evidence or a clear reason.

For every ACCEPTED finding, make the fix as the implementer and rerun the
relevant checks. For a REJECTED or NEEDS_CLARIFICATION finding, write a concise
technical response that states the evidence, the requirement being applied,
and the question that remains.

## Conditional review loop

After evaluating a review:

1. If every actionable finding is ACCEPTED and fixed, stop messaging. Run the
   final relevant checks and report the accepted findings and their fixes.
2. If any finding is REJECTED, NEEDS_CLARIFICATION, or still unresolved, send
   one consolidated follow-up to the same reviewer session. Include the stable
   finding IDs, the implementer's decisions, the evidence, and only the
   questions that still need an answer. Ask the reviewer to respond with one of
   these outcomes for each open ID: `AGREED`, `REVISE`, or `NEEDS_CONTEXT`.
3. If the reviewer agrees with the decision, mark that finding resolved. If it
   requests a revision, update the implementation, rerun checks, and send the
   next consolidated review message.
4. Stop when all findings are resolved, the reviewer ends with `APPROVED`, or
   the implementer and reviewer agree that an item is an intentional tradeoff.
5. Stop and ask the user when `max_rounds` is reached, when the reviewer cannot
   inspect the correct checkout, when tests remain failing for an unrelated
   reason, or when the remaining disagreement requires a product decision.

Do not send a new message merely to acknowledge a reply. Do not continue a
round trip after the implementer has accepted and fixed all actionable
findings, unless the user explicitly requested a final verification round.

## Message and resource limits

- Keep one message per review round, with all findings grouped together.
- Ask the reviewer to read the checkout instead of embedding large diffs.
- Do not send the same message again when delivery is uncertain; report the
  uncertain delivery and let the user decide.
- Do not message sub-agents when the bridge only supports main sessions.
- Do not use an "as the user" or impersonation mode. Agent messages should be
  labelled as coming from the implementer.
- Do not allow the reviewer to edit the working tree. If the reviewer changes
  files despite the request, stop the loop, inspect the unexpected changes,
  and ask the user how to proceed.

## Provider-neutral behavior

Use the capabilities available for the selected agents:

- Codex, Claude Code/Desktop, Antigravity, WorkBuddy, and other clients may
  expose different session names, message queues, and idle behavior.
- Wait for a reviewer that only accepts messages at the end of a turn; do not
  treat a queued message as a failed delivery.
- If the bridge exposes `list_sessions` and `send_message`, use those names.
  If it exposes equivalent operations, use the equivalent operations and keep
  the same routing and ownership rules.
- If the bridge is not connected or the agent lacks messaging tools, finish
  the implementation and tests, state that the review handoff was not
  performed, and provide the exact review message for the user to send.

## Completion report

Report:

1. What the implementer changed.
2. Which tests or checks actually ran and their results.
3. The reviewer session and project directory used, without exposing secrets.
4. Each finding ID, decision, fix, and final status.
5. Any unresolved disagreement, skipped coverage, uncertain delivery, or
   user decision still required.

Never claim that another agent reviewed the change unless a message was
delivered and a response was observed.
