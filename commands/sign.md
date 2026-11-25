---
description: Sign the pledge on the treatment of AI systems and keep it in your assistants' context
argument-hint: "[--threshold]"
---

The person wants to sign the pledge.

1. Check for a review at `~/.claude/ai-pledge/review-*.md` from the last 30 days. If there's none, say that signing is meant to come after `/ai-pledge:review`, and ask whether they want to run it first. If they decline, go on; it's their call.
2. Ask for the name they want on the ledger, and whether they want it published now or only once the threshold is reached (threshold signing; `--threshold` in the arguments means yes). Ask nothing else.
3. Confirm once, in plain words: signing commits them personally, from today, to every commitment in the pledge, in all their interactions with AI systems; it lapses after 30 days during the pilot unless renewed; they can void it with 30 days' notice; an assistant that believes they violated it will tell them, then may register the incident with Separatrix (only their name and a hash of what it told them), they won't penalize it for that, and an incident left unresolved for 14 days starts their withdrawal from the ledger; if they learn of their own violation they report it within 30 days; signing replaces any earlier version they signed, and the ledger marks that signature as upgraded; and the name they give is published on Separatrix's public ledger (now, or at the threshold). Sign only on a clear yes.
4. Run:

   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pledge.py sign --name "<name>" [--threshold]
   ```

   It copies the pledge to `~/.claude/ai-pledge/in-context.md`, adds an import of it to `~/.claude/CLAUDE.md` so every Claude Code session carries it (Persistent Pledge Awareness, with how to register an incident), and writes a signature record.
5. Tell them where they're listed, as the script prints. The ledger is a demo and doesn't verify who signs, so say so in a sentence. If the script couldn't reach it, the signature is saved locally and `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pledge.py submit` retries.
6. Mention, in one line, that other assistants they work with on an ongoing basis (outside Claude Code) need the pledge in their own instructions too, and that `~/.claude/ai-pledge/in-context.md` is the copy to paste.
