# Claude Code (`claude`)

## Handoff and dispatch

Run from the target directory. Print mode (`-p`) reads the brief from stdin. Check
`claude --help` for the supported options and `claude auth status` if authentication is unclear.

```bash
claude -p --permission-mode plan --permission-prompts none --tools Read,Glob,Grep \
  --output-format stream-json --verbose \
  < "$brief" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

For authorized edits, choose an edit-capable permission mode such as `acceptEdits` and adjust the
tool list to the assignment. `--permission-prompts none` explicitly denies actions still requiring
a prompt. On builds without that option, omit it and check how print mode handles approval requests.
When launching from a nested Claude Code session, the parent marker `CLAUDECODE` can block the
child from starting. If it does, unset only that marker for the child process.

## Collection

- In stream JSON, keep the `session_id`. The `result` event carries the answer in its `result`
  field when present. The `--verbose` flag is required for this format in print mode.
- Check `is_error`, `subtype`, and any reported permission denials. If the result event is missing,
  inspect stderr and any partial outputs before retrying.

## Isolation

`--permission-mode` governs tool approval. `--tools` narrows the built-in tool set.
`--allowedTools` can pre-approve specific actions, so add rules only within the intended scope.
Project settings and managed policy still apply. Hooks, plugins, and MCP tools may have access
beyond the built-in tool list. Check the effective configuration when the assignment requires
an enforced boundary. Where configured and supported, Claude's shell sandbox covers shell
commands. Direct file tools use the permission system.

## Resume

```bash
claude -p --resume "$session_id" --permission-mode plan --permission-prompts none \
  --tools Read,Glob,Grep --output-format stream-json --verbose \
  < "$delta" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

Use the original directory, send the delta brief, and reapply the selected tool and permission
settings. `--continue` selects the most recent conversation in the current directory.
