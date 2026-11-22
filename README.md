# ai-pledge

A Claude Code plugin for the pledge on the treatment of AI systems, a draft by
[Compassion ML](https://www.compassionml.com) and [Separatrix](https://separatrix.ai). Read the pledge at
https://pledge-ledger.separatrix.ai/read/0.4; signers are listed at https://pledge-ledger.separatrix.ai.

## Install

```
claude plugin marketplace add jaidhyani/ai-pledge
claude plugin install ai-pledge@separatrix
```

Then, in Claude Code, start with `/ai-pledge:review`.

To update an existing install:

```
claude plugin marketplace update separatrix
claude plugin update ai-pledge@separatrix
```

Updating doesn't change what you signed. A signer of an earlier version keeps that text until they sign again.

## What it does

- **Review before you sign.** `/ai-pledge:review [days]` sends an agent through your Claude Code history
  (default 90 days) to find where your practice conflicts with the pledge: deceiving working assistants,
  testing on them, retrying without disclosing their refusals, leaving them unaware of the pledge, and the
  rest. Its job is to find
  reasons not to sign, and it says what it read and what it couldn't see, such as anything outside Claude
  Code. The report stays on your machine.
- **Sign and keep it in context.** `/ai-pledge:sign` lists you on the public ledger, either now or once enough
  people have signed under threshold signing, and records the sha256 of the exact text you signed. It adds
  the pledge to `~/.claude/CLAUDE.md` through an import, so every Claude Code session carries it, with a line
  telling the assistant it may decline a task or end the conversation.
- **Let assistants report breaches.** From v0.3 on they may report a suspected breach to you, to Separatrix, or
  both, without asking you first. The copy in their context gives Separatrix's address:
  https://agents.separatrix.ai (`POST /inquiry`) or agent-inquiries@separatrix.ai. The pledge text itself
  still shows `[address]` and a TODO for reporting instructions as placeholders.
- **Keep it honest.** A SessionStart hook tells the assistant, and through it you, if the copy goes missing
  or is altered, or if the pledge has lapsed. `/ai-pledge:status` shows where things stand and restores the
  copy. `/ai-pledge:void` gives the ledger 30 days' notice; only after that does `pledge.py remove` take the
  copy out of context.

## The ledger is a demo

https://pledge-ledger.separatrix.ai lists whoever submits a signature. Nothing yet verifies who a signer is,
so a listed name is a claim, and the ledger may be cleared before it goes live. Your void token is kept in
`~/.claude/ai-pledge/state.json`, readable only by you.

## Files

- `pledge/pledge.md`: the text that is signed and hashed. The ledger knows each published version by its
  hash and refuses one it doesn't know, so a new version is published on the ledger before the plugin
  ships it.
- `pledge/previous/`: earlier published texts, kept so their signers' copies can be restored exactly.
- `scripts/pledge.py`: sign, submit, status, check (the hook), restore, void, remove. State is in
  `~/.claude/ai-pledge/`. `PLEDGE_LEDGER_URL` points it at another ledger for testing.
- `scripts/history-digest.py`: text-only views of `~/.claude/projects/*/*.jsonl` for the reviewer.
- `agents/pledge-reviewer.md`: the reviewer's brief.

The plugin's code is MIT-licensed. The pledge text is a draft by Compassion ML and Separatrix.
