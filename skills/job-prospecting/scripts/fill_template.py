#!/usr/bin/env python3
"""Fill a template (CV, letter) from a JSON file — safely.

Usage: python3 fill_template.py templates/cv-one-column.html data.json -o CV_First_Last_Company_Position.html

Placeholders:
  {{key}}    plain text, HTML-escaped
  {{{key}}}  rich text: only <p> <ul> <li> <strong> <em> <br> allowed, without attributes; anything else is refused
  <!--section:key--> ... <!--/section:key-->   removed when "key" is missing or empty (optional section)
Refuses to write the file if a placeholder is left unfilled, or if the data still contains [TO COMPLETE] or
{{...}} (so an unfinished document can never be produced by mistake).
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ALLOWED = {"p", "ul", "li", "strong", "em", "br"}
UNFINISHED = re.compile(r"\[(TO COMPLETE|À COMPLÉTER|A COMPLETER|POR COMPLETAR|ZU ERGÄNZEN)\]|\{\{", re.I)


def check_rich(key, value):
    for tag, attrs in re.findall(r"<\s*/?\s*([a-zA-Z0-9]+)([^>]*)>", value):
        if tag.lower() not in ALLOWED or attrs.strip().rstrip("/").strip():
            sys.exit(f"Refused in '{key}': <{tag}{attrs}> (allowed: {', '.join(sorted(ALLOWED))}, no attributes)")
    if re.search(r"javascript:|&#|<!--|url\(", value, re.I):
        sys.exit(f"Refused in '{key}': script, numeric entity, comment or url() not allowed")


def fill(template, data):
    def empty(k):
        v = data.get(k)
        return v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v)

    out = re.sub(r"<!--section:(\w+)-->(.*?)<!--/section:\1-->",
                 lambda m: "" if empty(m.group(1)) else m.group(2), template, flags=re.S)
    problems = [f"{k}: unfinished text" for k, v in data.items() if isinstance(v, str) and UNFINISHED.search(v)]
    if problems:
        sys.exit("Not written — the data is not finished:\n  - " + "\n  - ".join(problems))

    def rich(m):
        k = m.group(1)
        if k not in data:
            sys.exit(f"Missing value for {{{{{{{k}}}}}}}")
        v = "".join(data[k]) if isinstance(data[k], list) else str(data[k])
        check_rich(k, v)
        return v

    def plain(m):
        k = m.group(1)
        if k not in data:
            sys.exit(f"Missing value for {{{{{k}}}}}")
        return html.escape(str(data[k]))

    out = re.sub(r"\{\{\{\s*(\w+)\s*\}\}\}", rich, out)
    out = re.sub(r"\{\{\s*(\w+)\s*\}\}", plain, out)
    if "{{" in out or "}}" in out:
        sys.exit("A placeholder is left in the output")
    return out


def utf8_output():
    """Windows consoles may not be UTF-8: never crash on ✅ or accented text."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    utf8_output()
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("template", type=Path)
    p.add_argument("data", type=Path, help="JSON object: placeholder -> value")
    p.add_argument("-o", "--out", type=Path, required=True)
    a = p.parse_args()
    data = json.loads(a.data.read_text(encoding="utf-8"))
    a.out.write_text(fill(a.template.read_text(encoding="utf-8"), data), encoding="utf-8")
    print(f"written: {a.out}")


if __name__ == "__main__":
    main()
