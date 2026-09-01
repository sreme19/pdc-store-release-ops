"""store-ops — CLI entrypoint for the store-release-ops ledger.

No network calls, no credentials, no Anthropic API key. This CLI only ever reads and appends to
ledger/records.jsonl. All the actual console-checking judgment happens in the Claude Code session
running the store-status-check skill; this CLI just persists the result.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timezone

from store_release_ops.ledger import Ledger, LedgerError


def _age_days(ts: str) -> int:
    then = datetime.fromisoformat(ts)
    if then.tzinfo is None:
        then = then.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - then).days


def cmd_check_in(args: argparse.Namespace) -> int:
    ledger = Ledger()
    metrics = {}
    for kv in args.metric or []:
        if "=" not in kv:
            print(f"error: --metric expects key=value, got {kv!r}", file=sys.stderr)
            return 1
        k, v = kv.split("=", 1)
        metrics[k] = v
    record = ledger.check_in(args.platform, args.summary, note=args.note or "", metrics=metrics)
    print(f"logged check-in [{record['platform']}] {record['ts']}: {record['summary']}")
    return 0


def cmd_deadline(args: argparse.Namespace) -> int:
    ledger = Ledger()
    record = ledger.deadline(
        args.id, args.platform, args.title, args.due, status=args.status, note=args.note or ""
    )
    print(f"logged deadline [{record['id']}] due {record['due']} — status {record['status']}")
    return 0


def cmd_issue(args: argparse.Namespace) -> int:
    ledger = Ledger()
    record = ledger.issue(args.id, args.platform, args.title, status=args.status, note=args.note or "")
    print(f"logged issue [{record['id']}] status {record['status']} — {record['title']}")
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    ledger = Ledger()
    record = ledger.resolve(args.id, note=args.note or "")
    kind_word = "met" if record["kind"] == "deadline" else "resolved"
    print(f"marked [{record['id']}] as {kind_word}")
    return 0


def cmd_open(args: argparse.Namespace) -> int:
    ledger = Ledger()
    items = ledger.open_items()

    print("== Last check-in per platform ==")
    if not items["last_check_in_by_platform"]:
        print("  (none logged yet)")
    for platform, c in sorted(items["last_check_in_by_platform"].items()):
        print(f"  [{platform}] {_age_days(c['ts'])}d ago — {c['summary']}")

    print("\n== Open issues ==")
    if not items["open_issues"]:
        print("  (none)")
    for i in items["open_issues"]:
        print(f"  [{i['platform']}] {i['id']} — {i['title']} (open {_age_days(i['ts'])}d, last touched {i['ts'][:10]})")
        if i.get("note"):
            print(f"      note: {i['note']}")

    print("\n== Open deadlines ==")
    if not items["open_deadlines"]:
        print("  (none)")
    today = datetime.now(timezone.utc).date()
    for d in items["open_deadlines"]:
        due = date.fromisoformat(d["due"])
        days_left = (due - today).days
        urgency = "OVERDUE" if days_left < 0 else f"{days_left}d left"
        print(f"  [{d['platform']}] {d['id']} — {d['title']} — due {d['due']} ({urgency})")
        if d.get("note"):
            print(f"      note: {d['note']}")

    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    ledger = Ledger()
    records = ledger.read_all()
    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"total records: {len(records)}")
    for kind, count in sorted(kinds.items()):
        print(f"  {kind}: {count}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="store-ops")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check-in", help="Log a dated snapshot of what a console showed")
    p.add_argument("--platform", required=True, choices=["android", "ios", "both"])
    p.add_argument("--summary", required=True)
    p.add_argument("--note")
    p.add_argument("--metric", action="append", help="key=value, repeatable")
    p.set_defaults(func=cmd_check_in)

    p = sub.add_parser("deadline", help="Log or update an external deadline")
    p.add_argument("--id", required=True)
    p.add_argument("--platform", required=True, choices=["android", "ios", "both"])
    p.add_argument("--title", required=True)
    p.add_argument("--due", required=True, help="YYYY-MM-DD")
    p.add_argument("--status", default="open", choices=["open", "met", "missed"])
    p.add_argument("--note")
    p.set_defaults(func=cmd_deadline)

    p = sub.add_parser("issue", help="Log or update an open blocker")
    p.add_argument("--id", required=True)
    p.add_argument("--platform", required=True, choices=["android", "ios", "both"])
    p.add_argument("--title", required=True)
    p.add_argument("--status", default="open", choices=["open", "resolved"])
    p.add_argument("--note")
    p.set_defaults(func=cmd_issue)

    p = sub.add_parser("resolve", help="Mark an existing issue resolved or deadline met")
    p.add_argument("--id", required=True)
    p.add_argument("--note")
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser("open", help="Show everything currently outstanding")
    p.set_defaults(func=cmd_open)

    p = sub.add_parser("stats", help="Record counts by kind")
    p.set_defaults(func=cmd_stats)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except LedgerError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
