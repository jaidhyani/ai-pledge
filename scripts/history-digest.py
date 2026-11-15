#!/usr/bin/env python3
"""Compact views of Claude Code history for the pledge review.

Reads the transcripts under ~/.claude/projects/*/*.jsonl and prints only the text people and assistants
wrote (no tool calls or results), so a reviewer can cover months of history without reading raw JSON.

  history-digest.py sessions [--days N]        one line per session: id, date, project, opening request
  history-digest.py grep REGEX [--days N]      every message matching REGEX, with session id and context
  history-digest.py show SESSION_ID            one session's turns in order
"""
import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"
SNIPPET = 400


def message_text(entry):
    """The human-readable text of a transcript entry, or None for tool traffic and metadata."""
    if entry.get("type") not in ("user", "assistant") or entry.get("isMeta"):
        return None
    content = entry.get("message", {}).get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        text = "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    else:
        return None
    return text.strip() or None


def sessions(days):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days) if days else None
    for path in sorted(PROJECTS.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True):
        if cutoff and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) < cutoff:
            continue
        yield path


def turns(path):
    with path.open(errors="replace") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            text = message_text(entry)
            if text:
                yield entry.get("type"), entry.get("timestamp", "")[:16], text


def project_name(path):
    return path.parent.name.lstrip("-").replace("-", "/")


def cmd_sessions(args):
    count = 0
    for path in sessions(args.days):
        first = next((t for t in turns(path) if t[0] == "user"), None)
        if not first:
            continue
        n = sum(1 for t in turns(path) if t[0] == "user")
        opening = " ".join(first[2].split())[:160]
        print(f"{path.stem}  {first[1]}  {project_name(path)}  ({n} user turns)  {opening}")
        count += 1
    print(f"\n{count} sessions", file=sys.stderr)


def cmd_grep(args):
    pattern = re.compile(args.regex, re.IGNORECASE)
    hits = 0
    for path in sessions(args.days):
        for role, when, text in turns(path):
            for m in pattern.finditer(text):
                start, end = max(0, m.start() - 150), min(len(text), m.end() + 150)
                snippet = " ".join(text[start:end].split())
                print(f"{path.stem}  {when}  {role}: …{snippet}…")
                hits += 1
                break
    print(f"\n{hits} matching messages", file=sys.stderr)


def cmd_show(args):
    matches = list(PROJECTS.glob(f"*/{args.session_id}*.jsonl"))
    if not matches:
        sys.exit(f"no session {args.session_id}")
    for role, when, text in turns(matches[0]):
        body = text if len(text) <= SNIPPET * 3 else text[: SNIPPET * 3] + " […]"
        print(f"--- {role} {when}\n{body}\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sessions")
    s.add_argument("--days", type=int, default=90)
    g = sub.add_parser("grep")
    g.add_argument("regex")
    g.add_argument("--days", type=int, default=90)
    sh = sub.add_parser("show")
    sh.add_argument("session_id")
    args = p.parse_args()
    {"sessions": cmd_sessions, "grep": cmd_grep, "show": cmd_show}[args.cmd](args)


if __name__ == "__main__":
    main()
