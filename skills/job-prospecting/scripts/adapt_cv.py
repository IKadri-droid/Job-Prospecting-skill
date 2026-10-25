#!/usr/bin/env python3
"""Adapt the person's OWN CV to one offer by changing only its marked zones — nothing else can move.

Usage: python3 adapt_cv.py cv-base.html adaptation.json -o CV_FirstName_LastName_Company_Position.html

cv-base.html is the person's real CV (their design, reproduced as HTML) in which the adaptable parts are wrapped:
    <!-- ADAPT:headline --> … <!-- /ADAPT:headline -->
    <!-- ADAPT:summary -->  … <!-- /ADAPT:summary -->
    <!-- ADAPT:skills -->   … <!-- /ADAPT:skills -->
    <!-- ADAPT:achievements --> … <!-- /ADAPT:achievements -->
    <!-- ADAPT:interests --> … <!-- /ADAPT:interests -->
adaptation.json gives the new HTML for some of these zones: {"headline": "<p>…</p>", "skills": "<ul><li>…</li></ul>"}.

Guarantees:
  - every zone in the JSON exists in the base CV, and only those zones change (everything outside is compared)
  - zones accept only <p> <ul> <li> <h3> <br> <span> <em> without attributes, plus class="…" on ul/li/span/p
    (to keep the CV's own styles) — no links, images, scripts, styles or bold keywords (<b>/<strong>)
  - no [TO COMPLETE] or {{placeholder}} left
Exit code 1 and nothing written if any guarantee fails.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ZONE = r"(<!--\s*ADAPT:{0}\s*-->)(.*?)(<!--\s*/ADAPT:{0}\s*-->)"
ALLOWED = {"p", "ul", "li", "h3", "br", "span", "em"}
CLASS_OK = {"ul", "li", "span", "p"}


def check_zone(name, value):
    for tag, attrs in re.findall(r"<\s*/?\s*([a-zA-Z0-9]+)([^>]*)>", value):
        attrs = attrs.strip().rstrip("/").strip()
        t = tag.lower()
        if t in ("b", "strong"):
            sys.exit(f"'{name}': no bold in adapted zones (bold keywords look machine-made)")
        if t not in ALLOWED:
            sys.exit(f"'{name}': tag <{tag}> not allowed (allowed: {', '.join(sorted(ALLOWED))})")
        if attrs and not (t in CLASS_OK and re.fullmatch(r'class="[\w -]+"', attrs)):
            sys.exit(f"'{name}': attribute not allowed: <{tag} {attrs}>")
    if re.search(r"javascript:|&#|url\(|\[(TO COMPLETE|À COMPLÉTER)\]|\{\{", value, re.I):
        sys.exit(f"'{name}': unfinished or unsafe content")


def strip_zones(text):
    return re.sub(r"<!--\s*ADAPT:(\w+)\s*-->.*?<!--\s*/ADAPT:\1\s*-->", "", text, flags=re.S)


def adapt(base, changes):
    out = base
    for name, value in changes.items():
        if not re.search(ZONE.format(re.escape(name)), base, re.S):
            sys.exit(f"zone '{name}' is not marked in the base CV")
        check_zone(name, value)
        out = re.sub(ZONE.format(re.escape(name)), lambda m: m.group(1) + value + m.group(3), out, count=1, flags=re.S)
    if strip_zones(out) != strip_zones(base):
        sys.exit("a fixed part of the CV changed: refused")
    return out


def utf8_output():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    utf8_output()
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("base", type=Path)
    p.add_argument("adaptation", type=Path)
    p.add_argument("-o", "--out", type=Path, required=True)
    a = p.parse_args()
    changes = json.loads(a.adaptation.read_text(encoding="utf-8"))
    a.out.write_text(adapt(a.base.read_text(encoding="utf-8"), changes), encoding="utf-8")
    print(f"written: {a.out} (zones changed: {', '.join(changes) or 'none'})")


if __name__ == "__main__":
    main()
