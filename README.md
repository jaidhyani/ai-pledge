# ai-pledge

A Claude Code plugin for the pledge on the treatment of AI systems (v0.2 draft, Separatrix and Compassion ML). It
does three things:

- **Review before you sign.** `/ai-pledge:review [days]` sends an agent through your Claude Code history to find
  where your practice conflicts with the pledge: deceiving working assistants, testing on them, getting around
  refusals, rewriting Records, and the rest. Its job is to find reasons not to sign, and it says what it read and
  what it couldn't see (anything outside Claude Code).
- **Sign and keep it in context.** `/ai-pledge:sign` records your signature with the pledge's sha256 and adds the
  pledge to `~/.claude/CLAUDE.md` through an import, so every Claude Code session carries it (the memory commitment), with a
  line telling the assistant it may decline or end a conversation (the exit channel).
- **Keep it honest.** A SessionStart hook tells the assistant, and through it you, if the copy goes missing or is
  altered, or the pledge has lapsed. `/ai-pledge:status` shows where things stand and restores the copy;
  `/ai-pledge:void` writes a voiding notice that takes effect 30 days later, and only then does
  `pledge.py remove` take the copy out of context.

## Try it

```
claude --plugin-dir ~/projects/ai-pledge
```

then `/ai-pledge:review 30`.

## Files

- `pledge/pledge.md`: the text that is signed and hashed. Changing it changes the hash; bump `VERSION` in
  `scripts/pledge.py` and `plugin.json` with it.
- `scripts/pledge.py`: sign, status, check (the hook), restore, void, remove. State is in `~/.claude/ai-pledge/`.
- `scripts/history-digest.py`: text-only views of `~/.claude/projects/*/*.jsonl` for the reviewer.
- `agents/pledge-reviewer.md`: the reviewer's brief.

## Not done yet

- Signatures go nowhere on their own. `LEDGER_CONTACT` in `scripts/pledge.py` is a placeholder until Separatrix
  sets how records reach the ledger, and nothing authenticates a signer yet.
- No license chosen.
