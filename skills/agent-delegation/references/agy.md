# Antigravity (`agy`)

## Handoff and dispatch

Check `agy --help` for your version. Run from the target directory and declare it with an absolute
`--add-dir` path. Use `--new-project` for a fresh project or `--project` for a specified one.

```bash
agy --new-project --add-dir "$PWD" --log-file "$run_dir/agy.log" \
  --print="$(cat "$brief")" > "$run_dir/final.txt" 2> "$run_dir/stderr.log"
```

With text input, use the `--print=value` form so a brief starting with a hyphen stays the option
value. The brief is visible in process arguments and subject to OS argument length limits. Keep
sensitive text out of argv. For larger inputs, if your build supports it, check the stdin protocol
for `--input-format stream-json` with `--output-format stream-json`. A file reference is another
option if the agent can access the file.

Use `--print-timeout` if the run needs a time limit and the installed build supports it.

## Collection

- The command above captures the response on stdout and diagnostic output on stderr. With
  `--log-file`, look for a conversation ID in lines such as `Print mode: conversation=…` or
  `Created conversation …`.
- Print mode can deny an action requiring an interactive approval. Check stderr and the log
  when output is empty or incomplete. Inspect any requested artifacts and report blocked actions.

## Isolation

`--add-dir` declares a workspace. `--sandbox` enables terminal restrictions, with behavior
depending on the platform and build. Confirm how it affects writes before relying on it for a
writable or read-only run. Check non-terminal tools separately.

Start with ordinary permissions. `--dangerously-skip-permissions` auto-approves tool requests and
can widen access. Use it only with explicit authorization and a boundary suitable for the
assignment. If the installed build offers `--mode`, check what its selected mode permits in print
runs before relying on it. For example, agy 1.5.14 reports that `--mode plan` has no effect when
used with `--disable-slash-commands`.

## Resume

```bash
agy --conversation "$session_id" --log-file "$run_dir/agy.log" \
  --print="$(cat "$delta")" > "$run_dir/final.txt" 2> "$run_dir/stderr.log"
```

Reapply the intended runtime options and send the delta brief. Use the same working directory and
let `--conversation` select the saved project. `--continue` selects the most recent conversation.
Use it only when that is the desired one.
