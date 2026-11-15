---
description: Sign the pledge on the treatment of AI systems and keep it in your assistants' context
argument-hint: "[--threshold]"
---

The person wants to sign the pledge.

1. Check for a review at `~/.claude/ai-pledge/review-*.md` from the last 30 days. If there's none, say that signing is meant to come after `/ai-pledge:review`, and ask whether they want to run it first. If they decline, go on; it's their call.
2. Ask for the name they want on the ledger, and whether they want it published now or only once the threshold is reached (threshold signing; `--threshold` in the arguments means yes). Ask nothing else.
3. Confirm once, in plain words: signing commits them personally, from today, to every commitment in the pledge, in all their interactions with AI systems; it lapses after 30 days during the pilot unless renewed; and they can void it with 30 days' notice. Sign only on a clear yes.
4. Run:

   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pledge.py sign --name "<name>" [--threshold]
   ```

   It copies the pledge to `~/.claude/ai-pledge/pledge.md`, adds an import of it to `~/.claude/CLAUDE.md` so every Claude Code session carries it (the memory commitment), and writes a signature record.
5. Show the person the record and tell them how to send it to the ledger, as the script prints. The ledger doesn't verify signatures yet, so the record matters only once Separatrix has it.
6. Mention, in one line, that other assistants they work with on an ongoing basis (outside Claude Code) need the pledge in their own instructions too, and that `~/.claude/ai-pledge/pledge.md` is the copy to paste.
