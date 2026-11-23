# Pi (`pi`)

## Handoff and dispatch

Run from the target directory. Pass the brief on stdin and use `--mode json` for machine-readable
events. Check `pi --help` for your version. If authentication is unclear, use
`pi auth check --provider "$provider"` or `pi auth check --model "$model"` where supported.

```bash
pi --mode json --no-approve --tools read,grep,find,ls \
  < "$brief" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

Adjust the tool list to the assignment. Omitting `--tools` uses Pi's default tools, which may
include edits and shell commands. Use the configured model or select one with `--model`.

## Collection

- Read the `id` from the JSONL session header. Read assistant text content from completed message
  events. Streaming updates can repeat that content.
- Check `stopReason` on the assistant message. `error` and `aborted` indicate failure even if
  the process exits zero. Check stderr and any requested outputs.

## Isolation

Pi runs with the host process's access. `--tools` limits callable tools. `--no-approve` skips
project-local resources subject to trust. Loaded extensions can still run with host access.
Where supported, `--no-extensions` suppresses extension discovery. Use a host boundary if the
assignment requires enforced isolation.

## Resume

```bash
pi --mode json --no-approve --tools read,grep,find,ls --session "$session_id" \
  < "$delta" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

Run from the original directory, send the delta brief, and reapply the intended tools and trust
settings. Use the full ID or exact session path. `--continue` selects the most recent session
for the directory. Record the session identifier the resumed run reports.
