# Agent Delegation

Hand work to a separate CLI agent and get the requested result back. The skill covers preparing the handoff, choosing access, collecting outputs, and resuming a session. Your request defines the assignment and what should happen with the result.

## Usage

```text
> Delegate the task below to Codex and return its reply verbatim.
> Ask Claude Code for a second opinion on the following.
> Give agy and Pi the same assignment independently, then compare their responses.
> Resume the OpenCode session with this update.
```

Name a CLI if you have a preference. For continuation, give the session ID when you have it. The skill can also use an available CLI that fits your request when you leave the choice open.

Start with [SKILL.md](skills/agent-delegation/SKILL.md). It links to the handoff and result guides and to the commands for each supported CLI.

| CLI | Reference |
| --- | --- |
| Codex | [codex](skills/agent-delegation/references/codex.md) |
| Claude Code | [claude](skills/agent-delegation/references/claude.md) |
| OpenCode | [opencode](skills/agent-delegation/references/opencode.md) |
| Pi | [pi](skills/agent-delegation/references/pi.md) |
| Antigravity | [agy](skills/agent-delegation/references/agy.md) |

## Install

### Option 1: `npx skills` (works with most agents)

```bash
npx skills add haowang02/agent-delegation
```

Install for several agents at once without prompts:

```bash
npx skills add haowang02/agent-delegation -g -y -a claude-code -a codex -a opencode -a antigravity -a pi
```

### Option 2: Claude Code plugin

```text
/plugin marketplace add haowang02/agent-delegation
/plugin install agent-delegation@agent-delegation
```

### Option 3: Codex skill installer

```text
$skill-installer install https://github.com/haowang02/agent-delegation/tree/main/skills/agent-delegation
```

### Option 4: Manual

```bash
git clone https://github.com/haowang02/agent-delegation.git ~/.local/share/agent-delegation
for d in ~/.claude/skills ~/.agents/skills ~/.gemini/config/skills; do
  mkdir -p "$d" && ln -sfn ~/.local/share/agent-delegation/skills/agent-delegation "$d/agent-delegation"
done
```

## Requirements

Use a shell and at least one supported CLI installed and configured for its provider. Check that the selected CLI can reach the inputs and enforce any boundaries your task requires. The skill itself ships as Markdown, and its command examples use Bash-compatible syntax.

## Validation

Run `python3 -m unittest discover -s tests -v` to check skill packaging, links, and the availability of core flags in locally installed CLIs. Help output checks option availability. Provider access, effective permissions, and result formats can vary by installation.

## License

MIT
