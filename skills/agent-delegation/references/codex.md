# Codex (`codex`)

## Handoff and dispatch

Check `codex exec --help` for your version and `codex login status` if authentication is unclear.
Run from the target directory or pass `-C` to `codex exec`. Use `-` to read the brief from stdin.

```bash
codex exec --json -o "$run_dir/final.md" -s read-only - \
  < "$brief" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

Use `-s workspace-write` when the assignment authorizes changes to the workspace. Add
`--skip-git-repo-check` when running outside a Git repository. Let the configured model stand unless
there is a reason to select one with `-m`.

## Collection

- The `-o` file contains the final assistant message. Stdout contains JSONL events, including
  `thread.started` with the `thread_id` to keep for resume.
- Check stderr and events such as `turn.failed` or `error` when the run is interrupted or output is
  missing. Check requested artifacts separately, even if the final message is missing.

## Isolation

`-s` controls sandboxed command access. `read-only` restricts writes and `workspace-write` permits
writes to configured writable paths. Network access depends on the effective policy. If authorized
and necessary, `-c sandbox_workspace_write.network_access=true` enables network access for that
sandbox where supported. Check any active connectors or other tools separately when their access
matters.

Codex may load project instructions and configuration. On supported builds
`--ignore-user-config` skips the user config, and `-c project_doc_max_bytes=0` skips project
instructions. Use these only when appropriate to the assignment.

## Resume

```bash
codex exec --json -o "$run_dir/final.md" -s read-only resume "$session_id" - \
  < "$delta" > "$run_dir/events.jsonl" 2> "$run_dir/stderr.log"
```

Run from the original workspace. Send the delta brief and reapply the intended sandbox and other
overrides. If the build rejects an option, compare `codex exec --help` and
`codex exec resume --help` to check where it belongs. `--last` selects the latest matching session,
so use it only if you can identify that session.
