# Check and return the result

Use the requested handoff to decide how much to do after the CLI returns. A verbatim relay can end
with the response and its status. A verified result needs evidence against the assignment. A request
to integrate or publish work also needs the relevant authorization.

## Identify what came back

- Check the exit status and the completion or error indicators described in the CLI reference.
  A zero exit code can coexist with denied tools, missing output, or an incomplete result.
- Locate the response or output named in the brief. CLI events and progress messages can help locate
  it. Inspect the actual output when the assignment depends on it.
- Apply the checks relevant to the requested role. For a claim, consult its source if verification
  was requested. For an artifact, open it and check the requested content or behavior. For a shared
  workspace change, compare with its starting state and account for pre-existing work.
- Report material gaps, denied actions, and checks you could not perform. Attribute claims to the
  delegated agent when you are relaying its answer.

## Recover incomplete runs

If the process is still active, use its handle to monitor or steer it as the CLI allows. A cancelled,
failed, or timed-out run can leave changes or complete an external action before returning. Check
what happened before retrying, especially if repeating the action could apply it twice.

Resume a usable session when its context helps with the correction. Send the missing or corrected
instructions and keep the same authorization boundary. Start a fresh run when existing context
would mislead the recipient or the session is unavailable. Preserve existing work when deciding
where the new run should operate.

## Finish the requested handoff

Return the answer, artifact location, or run status the user asked for. Include any necessary follow-up,
such as unresolved issues or the CLI and session ID for resumption. When asked to combine results,
resolve differences using the task's criteria and the available evidence. Leave decisions and actions
with the party the user assigned them to.
