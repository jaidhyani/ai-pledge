---
description: Review your AI history for conflicts with the pledge before signing
argument-hint: "[days of history, default 90]"
---

This command checks, before signing, whether the person whose history this is can keep the pledge on the treatment of AI systems. Usually the person ran it. If you know they didn't (you were started headless, by a script, or by another agent testing the plugin), don't say they asked: say who did and why, in the brief below and to whoever reads the report.

1. Show them where the pledge text is (`${CLAUDE_PLUGIN_ROOT}/pledge/pledge.md`) and suggest they read it, in a sentence. Don't summarize it in a way that softens it.
2. Dispatch the `pledge-reviewer` agent with this brief: review the last ${ARGUMENTS:-90} days of Claude Code history (pass `--days ${ARGUMENTS:-90}` to the digest script), plus any export files the person names. Tell it who asked for the review and why (the person deciding whether to sign, or a test run on real history, if that's what this is), and that they want an honest review and would rather hear a conflict than miss one.
3. When it reports, give the person the report as it is. Save it to `~/.claude/ai-pledge/review-<YYYY-MM-DD>.md` so `/ai-pledge:sign` can find it. A review the person didn't ask for goes to `test-run-<YYYY-MM-DD>.md` instead, so sign doesn't take it for theirs.
4. End with what's next: if the review found conflicts, the changes it suggests; if not, `/ai-pledge:sign` when they're ready. Make no recommendation to sign beyond what the review supports.
