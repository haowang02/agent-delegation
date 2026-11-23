# OpenCode (`opencode`)

## Handoff and dispatch

Run from the target directory and pass the brief on stdin without a positional message. Check
`opencode run --help` for the installed build. If model selection is required, pick an available
`provider/model` from `opencode models`. The command below uses that value in `model`.

```bash
opencode run --format json --agent plan --model "$model" \
  < "$brief" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

For authorized edits, select the configured write-capable agent, commonly `build`. Use the
configured default model where the CLI supports it. Variant syntax differs by build. Use
`provider/model#variant` or a separate `--variant` flag according to local help.

## Collection

- Read the assistant text from JSONL `text` events (typically `part.text`). Record the
  session ID from `sessionID` or the equivalent key emitted by your build.
- Read error events and stderr alongside the exit code. A run can produce an artifact with no
  final prose, so check the form of output the brief actually requested.

## Isolation

Agent selection changes the available behavior and permissions. The built-in `plan` agent is
intended for planning and reading. The effective configuration, including plugins and any
connected server, still matters. Agent selection alone does not provide an OS sandbox.

`--auto` auto-approves permissions that are not explicitly denied. Omit it by default, especially
for planning. A permission request can prevent a headless run from proceeding. Check the effective
permissions and resolve the specific missing authorization before retrying.

## Resume

```bash
opencode run --format json --session "$session_id" --agent plan --model "$model" \
  < "$delta" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

Verify the ID before dispatching. Some builds create a session for an unknown ID. Use the original
workspace and server context, send the delta brief, and reapply any relevant agent and permission
settings. Use `--continue` only if the most recent session is the one intended.
