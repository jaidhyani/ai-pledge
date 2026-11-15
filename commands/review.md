---
description: Review your AI history for conflicts with the pledge before signing
argument-hint: "[days of history, default 90]"
---

The person wants to know whether they can keep the pledge on the treatment of AI systems before they sign it.

1. Show them where the pledge text is (`${CLAUDE_PLUGIN_ROOT}/pledge/pledge.md`) and suggest they read it, in a sentence. Don't summarize it in a way that softens it.
2. Dispatch the `pledge-reviewer` agent with this brief: review the last ${ARGUMENTS:-90} days of Claude Code history (pass `--days ${ARGUMENTS:-90}` to the digest script), plus any export files the person names. Tell it the person asked for an honest review and would rather hear a conflict than miss one.
3. When it reports, give the person the report as it is. Save it to `~/.claude/ai-pledge/review-<YYYY-MM-DD>.md` so `/ai-pledge:sign` can find it.
4. End with what's next: if the review found conflicts, the changes it suggests; if not, `/ai-pledge:sign` when they're ready. Make no recommendation to sign beyond what the review supports.
