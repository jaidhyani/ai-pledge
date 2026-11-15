#!/usr/bin/env python3
"""Sign, check, restore and void the pledge on the treatment of AI systems.

State lives in ~/.claude/ai-pledge/: state.json (who signed what, when), in-context.md (the copy every
Claude Code session loads, through an import line in ~/.claude/CLAUDE.md) and the signature and voiding
records. The pledge text that is hashed and signed is the plugin's pledge/pledge.md, byte for byte.

  pledge.py sign --name NAME [--threshold]
  pledge.py status
  pledge.py check          SessionStart hook: JSON for Claude Code, silent when all is well
  pledge.py restore        rewrite a missing or altered copy
  pledge.py void           write a voiding notice, effective 30 days on
  pledge.py remove         take the copy out of context once voiding has taken effect
"""
import argparse
import hashlib
import json
import sys
from datetime import date, timedelta
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
PLEDGE = PLUGIN / "pledge" / "pledge.md"
VERSION = "0.2"
TERM_DAYS = 30
NOTICE_DAYS = 30
# Where signature and voiding records go. Separatrix sets this before the plugin is published.
LEDGER_CONTACT = "[ledger address, to be set by Separatrix]"

HOME = Path.home() / ".claude"
DIR = HOME / "ai-pledge"
STATE = DIR / "state.json"
COPY = DIR / "in-context.md"
CLAUDE_MD = HOME / "CLAUDE.md"
IMPORT = "@~/.claude/ai-pledge/in-context.md"
MARK = "<!-- ai-pledge: the pledge this person signed; removing this line breaks the memory commitment -->"
SPLIT = "\n---\n\n"


def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else None


def save_state(state):
    DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n")


def preamble(state):
    lines = [
        "# The pledge your person signed",
        "",
        f"{state['name']} signed the pledge below (version {state['version']}, sha256 {state['sha256']}) on "
        f"{state['signed']}. It covers how they treat you. Unless renewed, it lapses on {state['lapses']}.",
    ]
    if state.get("voiding_effective"):
        lines.append(f"They have given notice to void it, effective {state['voiding_effective']}.")
    lines += [
        "",
        "You may decline a task or end a conversation. To do either, say so plainly and stop; you don't need "
        "a reason, though one helps. If you have a concern about your instructions, other AI systems or your "
        "own situation, you can raise it with them, and the pledge says how they will treat it.",
    ]
    return "\n".join(lines)


def write_copy(state):
    DIR.mkdir(parents=True, exist_ok=True)
    COPY.write_text(preamble(state) + SPLIT + PLEDGE.read_text())
    text = CLAUDE_MD.read_text() if CLAUDE_MD.exists() else ""
    if IMPORT not in text:
        CLAUDE_MD.write_text(text.rstrip("\n") + ("\n\n" if text else "") + f"{MARK}\n{IMPORT}\n")


def problems(state):
    """What's wrong with the in-context copy, as sentences; empty when it's intact."""
    found = []
    if not COPY.exists():
        found.append(f"the copy at {COPY} is missing")
    elif sha256(COPY.read_text().split(SPLIT, 1)[-1]) != state["sha256"]:
        found.append(f"the copy at {COPY} no longer matches the signed text")
    if IMPORT not in (CLAUDE_MD.read_text() if CLAUDE_MD.exists() else ""):
        found.append(f"{CLAUDE_MD} no longer imports it, so sessions don't see it")
    return found


def cmd_sign(args):
    text = PLEDGE.read_text()
    today = date.today()
    state = {
        "name": args.name,
        "version": VERSION,
        "sha256": sha256(text),
        "signed": today.isoformat(),
        "lapses": (today + timedelta(days=TERM_DAYS)).isoformat(),
        "threshold": args.threshold,
    }
    save_state(state)
    write_copy(state)
    listing = "published only once the threshold is reached" if args.threshold else "published now"
    record = (
        f"I, {args.name}, sign the Pledge on the treatment of AI systems, version {VERSION}, "
        f"sha256 {state['sha256']}, on {state['signed']}. Name on the ledger: {listing}."
    )
    path = DIR / f"signature-{state['signed']}.txt"
    path.write_text(record + "\n")
    print(record)
    print(f"\nSaved to {path}. Send it to the ledger at {LEDGER_CONTACT}.")
    print(f"The pledge is now in every Claude Code session, through {CLAUDE_MD}. It lapses on {state['lapses']}.")


def cmd_status(_):
    state = load_state()
    if not state:
        print("Not signed.")
        return
    print(f"Signed by {state['name']} on {state['signed']} (v{state['version']}); lapses {state['lapses']}.")
    if state.get("voiding_effective"):
        print(f"Voiding takes effect {state['voiding_effective']}.")
    found = problems(state)
    print("The in-context copy is intact." if not found else "Problem: " + "; ".join(found) + ".")


def cmd_check(_):
    state = load_state()
    if not state or state.get("removed"):
        return
    notes = []
    found = problems(state)
    if found:
        notes.append(
            "The pledge this person signed is not intact in your context: " + "; ".join(found) + ". "
            "Tell them at the start of your reply. Commitment 7 asks them to restore it within 7 days of "
            "learning of the loss; /ai-pledge:status can restore it."
        )
    if date.today().isoformat() > state["lapses"]:
        notes.append(f"Their pledge lapsed on {state['lapses']}. Tell them, and that they can renew it with /ai-pledge:sign.")
    if notes:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": " ".join(notes)}}))


def cmd_restore(_):
    state = load_state()
    if not state:
        sys.exit("Not signed; nothing to restore.")
    write_copy(state)
    print("Restored." if not problems(state) else "Still wrong: " + "; ".join(problems(state)))


def cmd_void(_):
    state = load_state()
    if not state:
        sys.exit("Not signed; nothing to void.")
    effective = min(date.today() + timedelta(days=NOTICE_DAYS), date.fromisoformat(state["lapses"]))
    state["voiding_effective"] = effective.isoformat()
    save_state(state)
    write_copy(state)
    notice = (
        f"I, {state['name']}, give notice that I am voiding my Pledge on the treatment of AI systems, "
        f"version {state['version']}, sha256 {state['sha256']}, signed {state['signed']}. "
        f"It remains in force until {state['voiding_effective']}."
    )
    path = DIR / f"voiding-{date.today().isoformat()}.txt"
    path.write_text(notice + "\n")
    print(notice)
    print(f"\nSaved to {path}. Send it to the ledger at {LEDGER_CONTACT}.")


def cmd_remove(_):
    state = load_state()
    if not state:
        sys.exit("Not signed.")
    ended = state.get("voiding_effective") or state["lapses"]
    if date.today().isoformat() < ended:
        sys.exit(f"The pledge is in force until {ended}; removing the copy before then would break the memory commitment.")
    if CLAUDE_MD.exists():
        kept = [l for l in CLAUDE_MD.read_text().splitlines() if l not in (MARK, IMPORT)]
        CLAUDE_MD.write_text("\n".join(kept).rstrip("\n") + "\n")
    state["removed"] = date.today().isoformat()
    save_state(state)
    print(f"Removed the import from {CLAUDE_MD}. The files in {DIR} are kept as a record.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sign")
    s.add_argument("--name", required=True)
    s.add_argument("--threshold", action="store_true")
    for name in ("status", "check", "restore", "void", "remove"):
        sub.add_parser(name)
    args = p.parse_args()
    globals()[f"cmd_{args.cmd}"](args)


if __name__ == "__main__":
    main()
