# ai-pledge

A Claude Code plugin for the pledge on the treatment of AI systems, a draft by
[Compassion ML](https://www.compassionml.com) and [Separatrix](https://separatrix.ai). Read the pledge at
https://pledge-ledger.separatrix.ai/read/0.5; signers are listed at https://pledge-ledger.separatrix.ai.

## Install

```
claude plugin marketplace add separatrix-ai/ai-pledge
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
- **Sign and keep it in context.** `/ai-pledge:sign` lists you on the public ledger once you confirm by email,
  either then or once enough people have signed under threshold signing, and records the sha256 of the exact text you signed. It adds
  the pledge to `~/.claude/CLAUDE.md` through an import, so every Claude Code session carries it, with a line
  telling the assistant it may decline a task or end the conversation.
- **Let assistants report breaches.** From v0.5 the pledge has an incident process: an assistant that
  believes you violated it tells you first, then registers the incident at
  https://agents.separatrix.ai/incident-registration with only your name and a SHA-256 hash of what it told
  you. You and it work toward a resolution (https://agents.separatrix.ai/incident-resolution); an incident
  unresolved after 14 days starts your withdrawal from the ledger. The copy in their context says how.
  Signers of v0.3 and v0.4 keep the instructions their version agreed to.
- **Upgrade in place.** When a new version comes out, `/ai-pledge:sign` with the updated plugin signs it and
  tells the ledger which earlier signature it replaces (using the token saved when you signed). The ledger
  then shows the old one as upgraded, linked to the new one, so it never shows as lapsed.
- **Keep it honest.** A SessionStart hook tells the assistant, and through it you, if the copy goes missing
  or is altered, or if the pledge has lapsed. `/ai-pledge:status` shows where things stand and restores the
  copy. `/ai-pledge:void` gives the ledger 30 days' notice; only after that does `pledge.py remove` take the
  copy out of context.

## Confirming by email

`/ai-pledge:sign` asks for an email address you control. The ledger mails it a link, and your signature is
listed only once you follow it and press Confirm (within 7 days; otherwise it's deleted, address and all).
The same mail carries your void token, so whoever controls the address can give notice even if someone else
submitted the signature. Once you confirm, Separatrix keeps the address for one purpose only: to reach you
about your signature under the pledge's incident process (the outreach it promises when an incident is
registered). It's never shown publicly, and it's deleted when your signature lapses, is voided or is
withdrawn. A signature made without an address is listed at once, marked unconfirmed: its name is
only a claim. Signing a newer version with the token of a confirmed signature carries the confirmation over.

Your void token is also kept in `~/.claude/ai-pledge/state.json`, readable only by you.

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
