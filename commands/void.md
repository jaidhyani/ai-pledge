---
description: Void your pledge, with the 30 days' notice it requires
---

The person wants to void their pledge.

1. Confirm once: the pledge stays in force for 30 days after the ledger receives their notice (or until it would lapse, if sooner), and the in-context copy stays in place until then, so their assistants keep seeing it.
2. On a clear yes, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pledge.py void`. It gives notice to the ledger, which sets the effective date and shows it publicly, and saves the notice locally.
3. Show them the notice and where the ledger shows it. Tell them that on or after the effective date, `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pledge.py remove` takes the copy out of their context.
