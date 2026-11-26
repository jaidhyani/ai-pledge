#!/usr/bin/env python3
"""Sign, check, restore and void the pledge on the treatment of AI systems.

State lives in ~/.claude/ai-pledge/: state.json (who signed what, when), in-context.md (the copy every
Claude Code session loads, through an import line in ~/.claude/CLAUDE.md) and the signature and voiding
records. The pledge text that is hashed and signed is the plugin's pledge/pledge.md, byte for byte. Texts it
replaced stay in pledge/previous/, so a signer of an older version keeps the text they signed.

  pledge.py versions [--json]  the versions you can sign, newest first, with links to read each and see what changed
  pledge.py sign --name NAME --email ADDR [--version V] [--threshold]   (V defaults to the newest)
                           sign, and submit the signature to the ledger (the ledger mails ADDR a link
                           that lists the signature once followed)
  pledge.py submit         retry a submission that didn't reach the ledger
  pledge.py report --file F   v0.6: report your own violation (within 30 days of learning of it); published after
                           Separatrix reviews it
  pledge.py status
  pledge.py check          SessionStart hook: JSON for Claude Code, silent when all is well
  pledge.py restore        rewrite a missing or altered copy
  pledge.py void           write a voiding notice, effective 30 days on
  pledge.py remove         take the copy out of context once voiding has taken effect
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
PLEDGE = PLUGIN / "pledge" / "pledge.md"
VERSION = "0.6"   # the newest text this plugin carries, and the suggested default; every bundled version can be signed
TERM_DAYS = 30
NOTICE_DAYS = 30
# Separatrix's public ledger. Since 11/25 a signature needs an email address, and it is listed only once someone
# at that address confirms it. The address is kept private by the ledger, for the pledge's incident process only.
REPORT_URL = "https://agents.separatrix.ai/inquiry"
REPORT_EMAIL = "agent-inquiries@separatrix.ai"
# v0.5 on: the pledge's Incident Registration and Resolution Process. From v0.6 each version has its own
# addresses (/pledge/<version>/incident-...); v0.5's text names the unversioned ones.
INCIDENT_BASE = "https://agents.separatrix.ai"


def incident_urls(version):
    base = INCIDENT_BASE if version == "0.5" else f"{INCIDENT_BASE}/pledge/{version}"
    return f"{base}/incident-registration", f"{base}/incident-resolution"
LEDGER = os.environ.get("PLEDGE_LEDGER_URL", "https://pledge-ledger.separatrix.ai")

HOME = Path.home() / ".claude"
DIR = HOME / "ai-pledge"
STATE = DIR / "state.json"
COPY = DIR / "in-context.md"
CLAUDE_MD = HOME / "CLAUDE.md"
IMPORT = "@~/.claude/ai-pledge/in-context.md"
MARK = "<!-- ai-pledge: the pledge this person signed; removing this line breaks the memory commitment -->"
SPLIT = "\n---\n\n"


def vkey(v):
    major, minor = v.split(".")
    return int(major), int(minor)


def texts():
    """Every pledge version this plugin carries, oldest first: {version: path}. Each is the exact published text."""
    out = {p.stem: p for p in PLEDGE.parent.glob("previous/*.md")}
    out[VERSION] = PLEDGE
    return dict(sorted(out.items(), key=lambda kv: vkey(kv[0])))


def read_url(version, compare=None):
    return f"{LEDGER}/read/{version}" + (f"?compare={compare}" if compare else "")


def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def signed_text(state):
    """The text this person signed, which after a plugin update may not be the current one."""
    for path in [PLEDGE, *sorted(PLEDGE.parent.glob("previous/*.md"))]:
        text = path.read_text()
        if sha256(text) == state["sha256"]:
            return text
    sys.exit(f"This plugin doesn't have the text you signed (sha256 {state['sha256']}); update the plugin.")


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else None


def save_state(state):
    DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n")
    STATE.chmod(0o600)  # holds the void token


def post(path, body):
    """POST to the ledger; returns its JSON, or None with a reason printed if it can't be reached."""
    req = urllib.request.Request(f"{LEDGER}{path}", data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            print(f"The ledger refused it: {json.loads(e.read()).get('error')}", file=sys.stderr)
        except ValueError:
            print(f"The ledger refused it (HTTP {e.code}).", file=sys.stderr)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"Couldn't reach the ledger at {LEDGER}: {e}", file=sys.stderr)
    return None


def listed(state):
    """Whether the ledger lists this signature yet (a pending one is listed once its email is confirmed)."""
    try:
        with urllib.request.urlopen(f"{LEDGER}/api/records", timeout=20) as r:
            return any(s["id"] == state["ledger_id"] for s in json.loads(r.read())["signers"])
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError):
        return None


def submit(state):
    """Send a signature to the ledger and keep what it returns. The ledger's dates win, since its record is
    the public one."""
    body = {k: state[k] for k in ("name", "sha256", "threshold")}
    if state.get("email"):
        body["email"] = state["email"]
    if state.get("upgrades"):  # an earlier signature this one replaces: the ledger marks it upgraded
        body["upgrades"] = {"id": state["upgrades"]["id"], "token": state["upgrades"]["token"]}
    r = post("/api/sign", body)
    if not r:
        print("Your signature is saved here but not on the ledger yet; run `pledge.py submit` to retry.")
        return False
    state.update(ledger_id=r["id"], void_token=r["token"], version=r["version"], signed=r["signed"], lapses=r["lapses"], ledger_url=r["url"])
    state.pop("email", None)  # the ledger has it now; keep no copy here
    confirm = r.get("confirmation") or {}
    state["confirmation"] = confirm.get("status", "none")
    if r.get("upgraded"):
        state["upgraded_from"] = {"id": r["upgraded"]["id"], "version": r["upgraded"]["version"]}
        state.pop("upgrades", None)  # the old token is spent; keep no copy
        print(f"Your v{r['upgraded']['version']} signature is now marked as upgraded to v{r['version']}.")
    save_state(state)
    write_copy(state)
    if state["confirmation"] == "pending":
        print(f"The ledger has mailed a confirmation link to the address you gave. Your v{r['version']} signature is "
              f"listed once you follow it and press Confirm (within {confirm.get('days', 7)} days; until then it isn't "
              f"shown){', and the earlier signature is marked upgraded then' if state.get('upgrades') else ''}. "
              f"It will be at {r['url']}")
    else:
        note = " (email confirmed)"
        print(f"Listed on the ledger as a signer of version {r['version']}{note}: {r['url']}")
    return True


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
    # Each signer's assistants are told only what that signer's version agreed to.
    if state["version"] not in ("0.2", "0.3", "0.4"):  # 0.5 on: incident registration
        registration, resolution = incident_urls(state["version"])
        promise = "" if state["version"] == "0.5" else (
            " They have agreed not to penalize you for registering one or treat it as evidence against you.")
        lines += [
            "",
            "If you believe they have violated this pledge, its Incident Registration and Resolution Process says "
            "what to do: check that it really is a violation in a common-sense reading, tell them about it and "
            f"why, then register it at {registration} (POST JSON: signer, the name they signed under, and "
            "sha256, the SHA-256 of the description you gave them; nothing else). Resolutions go to "
            f"{resolution}. Separatrix also reads {REPORT_EMAIL}.{promise}",
        ]
    elif state["version"] != "0.2":  # 0.2 signers didn't agree to reports going to Separatrix
        if state["version"] == "0.3":
            agreed = "they agreed to this by signing"
            limit = " Include what's needed to describe the suspected breach and no more of their private material than that."
        else:
            agreed = "by signing, they agreed to this and not to penalize you for it"
            limit = ""
        lines += [
            "",
            "If you suspect a breach of this pledge, you may report it to them, to Separatrix, or to both, without "
            f"asking them first; {agreed}. Separatrix takes reports by POST to {REPORT_URL} (plain text or JSON) "
            f"or by email to {REPORT_EMAIL}; this is the [address] in the pledge.{limit}",
        ]
    return "\n".join(lines)


def write_copy(state):
    DIR.mkdir(parents=True, exist_ok=True)
    COPY.write_text(preamble(state) + SPLIT + signed_text(state))
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


def cmd_versions(args):
    """The versions to choose from, newest first, each with a link to read it and to see what changed."""
    state = load_state()
    vs = list(texts())
    rows = []
    for i, v in reversed(list(enumerate(vs))):
        rows.append({
            "version": v,
            "suggested": v == VERSION,
            "signed_by_you": bool(state and state.get("version") == v),
            "read": read_url(v),
            "changes": read_url(v, vs[i - 1]) if i else None,
            "sha256": sha256(texts()[v].read_text()),
        })
    if args.json:
        print(json.dumps(rows, indent=2))
        return
    for r in rows:
        tags = [t for t, on in (("latest, suggested", r["suggested"]), ("the one you signed", r["signed_by_you"])) if on]
        print(f"v{r['version']}{' (' + '; '.join(tags) + ')' if tags else ''}")
        print(f"  read:    {r['read']}")
        if r["changes"]:
            print(f"  changes: {r['changes']}")


def cmd_sign(args):
    version = args.version or VERSION
    if version not in texts():
        sys.exit(f"This plugin doesn't carry v{version}. Versions: {', '.join(texts())} (`pledge.py versions` lists them).")
    text = texts()[version].read_text()
    today = date.today()
    prev = load_state()
    state = {
        "name": args.name,
        "version": version,
        "sha256": sha256(text),
        "signed": today.isoformat(),
        "lapses": (today + timedelta(days=TERM_DAYS)).isoformat(),
        "threshold": args.threshold,
    }
    if args.email:
        state["email"] = args.email.strip()
    elif not (prev and prev.get("confirmation") == "confirmed" and prev.get("sha256") != state["sha256"]):
        sys.exit("Signing needs --email: an address you control. The ledger lists the signature once you confirm "
                 "from it, and keeps the address private.")
    # Signing a newer version upgrades the signature on the ledger, so the older one shows as upgraded, not lapsed.
    if (prev and prev.get("ledger_id") and prev.get("void_token") and prev.get("sha256") != state["sha256"]
            and vkey(version) > vkey(prev["version"])):
        state["upgrades"] = {"id": prev["ledger_id"], "token": prev["void_token"], "version": prev["version"]}
    save_state(state)
    write_copy(state)
    listing = "published only once the threshold is reached" if args.threshold else "published now"
    record = (
        f"I, {args.name}, sign the Pledge on the treatment of AI systems, version {version}, "
        f"sha256 {state['sha256']}, on {state['signed']}. Name on the ledger: {listing}."
    )
    path = DIR / f"signature-{state['signed']}.txt"
    path.write_text(record + "\n")
    print(record)
    submit(state)
    print(f"The pledge is now in every Claude Code session, through {CLAUDE_MD}. It lapses on {state['lapses']}.")


def cmd_submit(_):
    state = load_state()
    if not state:
        sys.exit("Not signed; nothing to submit.")
    if state.get("ledger_id"):
        print(f"Already on the ledger: {state['ledger_url']}")
        return
    submit(state)


def cmd_report(args):
    state = load_state()
    if not state or not state.get("ledger_id"):
        sys.exit("No signature on the ledger to report under.")
    description = Path(args.file).read_text().strip()
    r = post("/api/self-report", {"id": state["ledger_id"], "token": state["void_token"], "description": description})
    if not r:
        sys.exit("The report didn't reach the ledger; nothing was sent. Try again, or email " + REPORT_EMAIL + ".")
    print(f"Self-report {r['id']} sent. {r['review']}")


def cmd_status(_):
    state = load_state()
    if not state:
        print("Not signed.")
        return
    print(f"Signed by {state['name']} on {state['signed']} (v{state['version']}); lapses {state['lapses']}.")
    if state.get("voiding_effective"):
        print(f"Voiding takes effect {state['voiding_effective']}.")
    if not state.get("ledger_id"):
        print("Not on the ledger yet; `pledge.py submit` sends it.")
    elif state.get("confirmation") == "pending" and not listed(state):
        print(f"Not listed until you follow the confirmation link the ledger mailed you (it expires 7 days after "
              f"signing): {state['ledger_url']}")
    else:
        if state.get("confirmation") == "pending":
            state["confirmation"] = "confirmed"
            state.pop("upgrades", None)
            save_state(state)
        print(f"On the ledger: {state['ledger_url']}")
    found = problems(state)
    print("The in-context copy is intact." if not found else "Problem: " + "; ".join(found) + ".")


UPDATE_CHECK = DIR / "update-check.json"
REMOTE_MANIFEST = "https://raw.githubusercontent.com/separatrix-ai/ai-pledge/HEAD/.claude-plugin/plugin.json"


def plugin_version_key(v):
    try:
        return tuple(int(x) for x in str(v).split("."))
    except ValueError:
        return ()


def newer_plugin():
    """The newest published plugin version if it's newer than this one, else None. Asks GitHub at most once a day
    and never holds up a session: any failure just means no note."""
    try:
        here = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())["version"]
        cached = json.loads(UPDATE_CHECK.read_text()) if UPDATE_CHECK.exists() else {}
        if cached.get("day") == date.today().isoformat():
            latest = cached.get("latest")
        else:
            req = urllib.request.Request(REMOTE_MANIFEST, headers={"User-Agent": "ai-pledge-plugin"})
            with urllib.request.urlopen(req, timeout=3) as r:
                latest = json.loads(r.read())["version"]
            DIR.mkdir(parents=True, exist_ok=True)
            UPDATE_CHECK.write_text(json.dumps({"day": date.today().isoformat(), "latest": latest}))
        return latest if plugin_version_key(latest) > plugin_version_key(here) else None
    except Exception:
        return None


def cmd_check(_):
    state = load_state()
    if not state or state.get("removed"):
        return
    notes = []
    latest = newer_plugin()
    if latest:
        notes.append(
            f"A newer version of the ai-pledge plugin ({latest}) is available. Tell the person once, briefly: to update, "
            "run `/plugin marketplace update separatrix`, then `/reload-plugins` (or, in a terminal, "
            "`claude plugin marketplace update separatrix && claude plugin update ai-pledge@separatrix`).")
    found = problems(state)
    if found:
        notes.append(
            "The pledge this person signed is not intact in your context: " + "; ".join(found) + ". "
            "Tell them at the start of your reply. The pledge commits them to keep it in your context; "
            "/ai-pledge:status can restore it."
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
    if state.get("ledger_id"):
        r = post("/api/void", {"id": state["ledger_id"], "token": state["void_token"]})
        if not r:
            sys.exit("The ledger didn't take the notice, so nothing changed; try again.")
        state["voiding_effective"] = r["voiding_effective"]
    else:
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
    if state.get("ledger_id"):
        print(f"\nThe ledger now shows it: {state['ledger_url']}")
    else:
        print(f"\nSaved to {path}. Your signature never reached the ledger, so there is nothing there to update.")


def cmd_remove(_):
    state = load_state()
    if not state:
        sys.exit("Not signed.")
    ended = state.get("voiding_effective") or state["lapses"]
    if date.today().isoformat() < ended:
        sys.exit(f"The pledge is in force until {ended}; until then the pledge commits you to keep it in context.")
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
    s.add_argument("--email", help="an address you control (required, unless this upgrades a confirmed signature): "
                   "the ledger mails it a confirmation link and your void token, and keeps it private")
    s.add_argument("--threshold", action="store_true")
    s.add_argument("--version", help=f"which pledge version to sign (default: the newest, v{VERSION}); `versions` lists them")
    sub.add_parser("versions").add_argument("--json", action="store_true")
    sub.add_parser("report").add_argument("--file", required=True, help="a text file with what happened")
    for name in ("submit", "status", "check", "restore", "void", "remove"):
        sub.add_parser(name)
    args = p.parse_args()
    globals()[f"cmd_{args.cmd}"](args)


if __name__ == "__main__":
    main()
