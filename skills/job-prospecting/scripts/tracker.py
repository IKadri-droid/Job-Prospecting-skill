#!/usr/bin/env python3
"""Keep the applications tracking table (tracking.csv) — add, update, list, and reminders due.

Usage:
  python3 tracker.py add --employer "Example Bakery" --title "Apprentice baker" --place Lyon --kind offer \
      --source "Employment service" --url https://… --contact jobs@example.org
  python3 tracker.py set <id> status=sent sent_on=2026-11-03
  python3 tracker.py list [--status sent]
  python3 tracker.py due [--days 7] [--holidays holidays.txt] [--today 2026-11-12]
Options: --file tracking.csv (default: ./tracking.csv, created with the right header if missing).

Statuses: to_prepare, ready_to_send, sent, waiting, reminder_to_approve, reminder_sent, reply_received, interview,
rejection, offer, no_reply. "due" lists applications sent N working days ago (weekends and the dates of the optional
holidays file excluded) with no reply and no reminder yet — the person writes and sends the reminder themselves.
Writes are atomic (temporary file then replace) so the table is never left half-written.
"""
import argparse
import csv
import io
import os
import re
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

COLUMNS = ["id", "employer", "title", "place", "kind", "source", "url", "contact", "status", "prepared_on", "sent_on",
           "reminder_on", "reply_on", "reply", "cv_file", "letter_file", "notes"]
STATUSES = ["to_prepare", "ready_to_send", "sent", "waiting", "reminder_to_approve", "reminder_sent", "reply_received",
            "interview", "rejection", "offer", "no_reply"]


def read(path):
    if not path.exists():
        return []
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig"))))


def write(path, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    fd, tmp = tempfile.mkstemp(dir=path.parent if str(path.parent) else ".", prefix=".tracking-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(buf.getvalue())
    os.replace(tmp, path)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "application"


def working_days_after(start, n, holidays):
    d = start
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in holidays:
            n -= 1
    return d


def utf8_output():
    """Windows consoles may not be UTF-8: never crash on ✅ or accented text."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    utf8_output()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=Path, default=Path("tracking.csv"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    for c in ("employer", "title", "place", "kind", "source", "url", "contact", "cv_file", "letter_file", "notes"):
        s.add_argument(f"--{c}", default="")
    s.add_argument("--status", default="to_prepare", choices=STATUSES)
    s = sub.add_parser("set")
    s.add_argument("id")
    s.add_argument("changes", nargs="+", help="field=value")
    s = sub.add_parser("list")
    s.add_argument("--status", choices=STATUSES)
    s = sub.add_parser("due")
    s.add_argument("--days", type=int, default=7)
    s.add_argument("--holidays", type=Path, help="one YYYY-MM-DD per line")
    s.add_argument("--today", type=date.fromisoformat, default=date.today())
    a = ap.parse_args()

    rows = read(a.file)
    if a.cmd == "add":
        if not a.employer:
            sys.exit("--employer is required")
        base = f"{date.today().isoformat()}-{slug(a.employer)}"
        ident, n = base, 2
        while any(r["id"] == ident for r in rows):
            ident, n = f"{base}-{n}", n + 1
        dup = [r for r in rows if r["employer"].lower() == a.employer.lower() and r["title"].lower() == a.title.lower()]
        if dup:
            sys.exit(f"already tracked: {dup[0]['id']} (same employer and title)")
        row = {c: getattr(a, c, "") or "" for c in COLUMNS}
        row.update(id=ident, status=a.status, prepared_on=date.today().isoformat() if a.status != "to_prepare" else "")
        rows.append(row)
        write(a.file, rows)
        print(f"added: {ident}")
    elif a.cmd == "set":
        row = next((r for r in rows if r["id"] == a.id or r["id"].startswith(a.id)), None)
        if not row:
            sys.exit(f"no application '{a.id}'")
        for ch in a.changes:
            k, _, v = ch.partition("=")
            if k not in COLUMNS or k == "id":
                sys.exit(f"unknown field: {k}")
            if k == "status" and v not in STATUSES:
                sys.exit(f"unknown status: {v} ({', '.join(STATUSES)})")
            if k.endswith("_on") and v:
                date.fromisoformat(v)
            if k == "reminder_on" and row.get("reminder_on"):
                sys.exit("only one reminder per application")
            row[k] = v
        write(a.file, rows)
        print(f"updated: {row['id']}")
    elif a.cmd == "list":
        for r in rows:
            if not a.status or r["status"] == a.status:
                print(f"{r['id']:<44} {r['status']:<20} {r['employer']} — {r['title']}")
    elif a.cmd == "due":
        holidays = set()
        if a.holidays:
            holidays = {date.fromisoformat(l.strip()) for l in a.holidays.read_text(encoding="utf-8").splitlines() if l.strip()}
        for r in rows:
            if r["status"] in ("sent", "waiting") and r["sent_on"] and not r["reply_on"] and not r["reminder_on"]:
                due = working_days_after(date.fromisoformat(r["sent_on"]), a.days, holidays)
                if a.today >= due:
                    print(f"{r['id']:<44} reminder due since {due} — {r['employer']} — {r['title']}")


if __name__ == "__main__":
    main()
