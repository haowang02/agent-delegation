---
name: agent-delegation
description: >-
  Delegates work to a separate CLI agent, collects its result, and resumes its sessions. Use for
  requests to delegate work to or get a second opinion from Codex, Claude Code, OpenCode, Pi, or
  Antigravity (agy), or when the user requests external CLI delegation without choosing a tool.
  Also use for follow-ups to these delegated sessions.
license: MIT
metadata:
  version: 0.0.1
---

# Agent Delegation

Carry the user's assignment across the process boundary. The user defines the work, the expected
outputs, and your role after dispatch.

## Choose the CLI

Use the CLI the user names. For a continuation, use the CLI and workspace of the existing session.
If the choice is open, use an available, configured CLI whose capabilities and permissions fit the
assignment. Follow the user's preferences about provider and model. If their chosen CLI is blocked,
report the blocker and confirm any material change before switching.

Use a shell and a supported CLI configured for its provider. Read the selected CLI's reference
before launching it. Check local help when an option depends on the installed version.

| CLI | Binary | Reference |
| --- | --- | --- |
| Codex | `codex` | [references/codex.md](references/codex.md) |
| Claude Code | `claude` | [references/claude.md](references/claude.md) |
| OpenCode | `opencode` | [references/opencode.md](references/opencode.md) |
| Pi | `pi` | [references/pi.md](references/pi.md) |
| Antigravity | `agy` | [references/agy.md](references/agy.md) |

The shell examples use `brief` for the absolute path to the prompt file and `run_dir` for a fresh
private output directory, which you can create with `run_dir=$(mktemp -d)`. Resume examples also
use `delta` for the follow-up prompt file and `session_id` for the recorded identifier. Adapt the
example's access settings to the assignment.

## Hand off and collect

1. **Give the agent enough context to act.** Pass the requested outcome, the relevant inputs it can
   reach, any constraints it needs to follow, and where to return the result. Share only information
   that can be sent to the selected provider. See [writing the brief](references/writing-the-brief.md)
   for an optional template and guidance on independent assignments.
2. **Launch with the appropriate access.** Match the CLI's workspace, tools, and permission settings
   to the actions the assignment authorizes. Enforced isolation depends on effective CLI and host
   controls. If the assignment needs a boundary you cannot enforce, report that blocker.
   For overlapping writes, give each run a separate target or coordinate their order.
3. **Capture the outcome.** Keep the process handle while it runs and the CLI's session identifier
   if it reports one. Capture the response, errors, and any requested outputs. Wait when the user
   expects a completed result. For dispatch-only handoffs, use the available background process
   facility and return the current status and any handle useful for follow-up.
4. **Return what the user asked for.** Distinguish launch, successful completion, and usable results.
   Pass through the result for a relay. If the user requests further work, use the evidence needed
   for that work and report any material gaps. See
   [checking and returning results](references/verify-and-deliver.md) for incomplete runs,
   verification, and integration.

## Continue a run

Once the prior turn has ended, use its exact session ID and send the update, including any changed
inputs or constraints. Preserve the intended workspace and reapply the relevant per-run options
from the CLI reference. Use a latest-session shortcut only when you can establish that it selects
the right session. If a run ended early, check for partial work or side effects before resuming or
starting a new run.
