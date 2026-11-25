---
description: Report your own violation of the pledge (v0.6, within 30 days of learning of it)
---

The person wants to report a violation of the pledge they made themselves. Under v0.6 (incident process, point 9), a Signer who learns of their own violation reports it within 30 days. Separatrix reviews the report before it is published on the ledger.

1. Ask what happened, in their words: when, which kind of AI Individual (Assistant, Test subject, External contact), which part of the pledge, and what they've done about it since. Leave out other people's private information and long quotes; the report is published.
2. Show them the text you'll send and get a clear yes. Say that it's published on the ledger, beside their signature, once Separatrix has reviewed it.
3. Write it to `~/.claude/ai-pledge/report-<YYYY-MM-DD>.md`, then run:

   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pledge.py report --file ~/.claude/ai-pledge/report-<YYYY-MM-DD>.md
   ```

4. Tell them the report id it prints, and that Separatrix reviews it before it's published.
