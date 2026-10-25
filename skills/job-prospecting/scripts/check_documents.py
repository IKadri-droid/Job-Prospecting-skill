#!/usr/bin/env python3
"""Check CVs and cover letters before the person sees them. Exit code 1 if a blocking problem is found.

Usage:
  python3 check_documents.py CV_….pdf --profile profile.md --missing "Forklift licence" "SAP"
  python3 check_documents.py Letter_….html --letter --employer "Example Bakery" --lang fr
  python3 check_documents.py CV_….pdf Letter_….pdf --profile profile.md --letter-file Letter_….pdf

Reads HTML, PDF (with pdftotext if installed) or plain text. Checks:
  - unfinished text: [TO COMPLETE], {{placeholder}}, Lorem ipsum
  - --missing: requirements the person does NOT have must not appear anywhere
  - --profile: certifications, licences and test scores named in the document must also be in the profile
    (built-in watch list + --watch FILE, one term per line)
  - banned stock phrases (en, fr, es, de)
  - letters: word count of the body (default 250–300), no bold, employer named (--employer), one page
  - CVs: at most 2 pages; bold keywords inside bullet points
  - file name: CV_FirstName_LastName_Company_Position.pdf / Letter_… (warning only)
If a check cannot run (e.g. no pdftotext for a PDF), it is reported as NOT CHECKED, never as passed.
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

WATCH = ["OSCP", "CEH", "CISSP", "CISM", "CCNA", "CCNP", "CompTIA", "Security+", "PMP", "PRINCE2", "ITIL",
         "Six Sigma", "Scrum Master", "PSM", "CPA", "ACCA", "CFA", "TOEIC", "TOEFL", "IELTS", "Cambridge",
         "DELF", "DALF", "TCF", "Goethe", "DELE", "HSK", "CACES", "HACCP", "SST", "BAFA", "BNSSA", "PSE1", "PSE2",
         "CDL", "forklift licence", "forklift license", "AWS Certified", "Azure Fundamentals", "Google Cloud Certified",
         "Salesforce Certified", "SAP certified", "IPAF", "CSCS", "NEBOSH", "IOSH", "Habilitation électrique",
         "permis C", "permis CE", "permis D", "FIMO", "FCO"]
BANNED = {
    "en": ["passionate about", "dynamic and motivated", "ideal candidate", "since i was a child", "great asset",
           "do not hesitate to contact", "don't hesitate to contact", "think outside the box", "hard-working and motivated"],
    "fr": ["passionné depuis", "passionnée depuis", "depuis toujours", "dynamique et motivé", "dynamique et motivée",
           "candidat idéal", "candidate idéale", "n'hésitez pas", "véritable atout", "force de travail"],
    "es": ["apasionado por", "apasionada por", "dinámico y motivado", "candidato ideal", "no dude en contactar"],
    "de": ["leidenschaftlich", "dynamisch und motiviert", "idealer kandidat", "zögern sie nicht"],
}
SALUTATION = r"^(dear|hello|madame|monsieur|bonjour|sehr geehrte|liebe|estimad[oa]s?|gentile|egregi|geachte|cher|chère)"
CLOSING = r"^(sincerely|kind regards|best regards|yours (faithfully|sincerely)|je vous prie|veuillez agréer|cordialement|" \
          r"mit freundlichen|atentamente|un saludo|cordiali saluti|met vriendelijke)"


def text_of(path, notes):
    p = Path(path)
    raw = p.read_bytes()
    if p.suffix.lower() == ".pdf":
        if not shutil.which("pdftotext"):
            notes.append(f"NOT CHECKED {p.name}: no pdftotext to read the PDF (check the HTML version instead)")
            return None, None
        txt = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
        return txt, None
    content = raw.decode("utf-8", "replace")
    if p.suffix.lower() in (".html", ".htm"):
        plain = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(style|script|title).*?</\1>", " ", content)))
        return plain, content
    return content, None


def pages(path):
    p = Path(path)
    if p.suffix.lower() != ".pdf":
        return None
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        if m:
            return int(m.group(1))
    return len(re.findall(rb"/Type\s*/Page[^s]", p.read_bytes())) or None


def letter_body_words(txt, html_src):
    if html_src:
        m = re.search(r'<div class="body">(.*?)</div>', html_src, re.S)
        if m:
            paras = re.findall(r"<p>(.*?)</p>", m.group(1), re.S)
            inner = paras[1:-1] if len(paras) >= 3 else paras  # without salutation and closing
            return len(html.unescape(re.sub(r"<[^>]+>", " ", " ".join(inner))).split())
    lines = [l.strip() for l in txt.splitlines()]
    start = next((i for i, l in enumerate(lines) if re.match(SALUTATION, l, re.I)), None)
    end = next((i for i, l in enumerate(lines) if start is not None and i > start and re.match(CLOSING, l, re.I)), None)
    if start is None or end is None:
        return None
    return len(" ".join(lines[start + 1:end]).split())


def present(term, txt):
    return re.search(rf"(?<![\w+#]){re.escape(term)}(?![\w+#])", txt, re.I) is not None


def utf8_output():
    """Windows consoles may not be UTF-8: never crash on ✅ or accented text."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    utf8_output()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--profile", type=Path, help="profile.md: certifications named in documents must be in it")
    ap.add_argument("--missing", nargs="*", default=[], help="requirements the person does not have")
    ap.add_argument("--watch", type=Path, help="extra terms to watch, one per line")
    ap.add_argument("--letter", action="store_true", help="treat every file as a letter")
    ap.add_argument("--letter-file", nargs="*", default=[], help="these files are letters (others are CVs)")
    ap.add_argument("--employer", help="the letter must name this employer")
    ap.add_argument("--lang", default="all", help="banned phrases language: en, fr, es, de or all")
    ap.add_argument("--min-words", type=int, default=250)
    ap.add_argument("--max-words", type=int, default=300)
    a = ap.parse_args()

    profile = a.profile.read_text(encoding="utf-8") if a.profile else None
    watch = WATCH + ([l.strip() for l in a.watch.read_text(encoding="utf-8").splitlines() if l.strip()] if a.watch else [])
    banned = [b for k, v in BANNED.items() if a.lang in ("all", k) for b in v]
    letters = {Path(f).name for f in a.letter_file}
    blocking = 0
    for f in a.files:
        notes, errors, warns = [], [], []
        txt, html_src = text_of(f, notes)
        name = Path(f).name
        is_letter = a.letter or name in letters or name.lower().startswith(("letter", "lettre", "lm_", "carta", "anschreiben"))
        if txt is not None:
            flat = re.sub(r"\s+", " ", txt)
            if re.search(r"\[(TO COMPLETE|À COMPLÉTER|A COMPLETER|POR COMPLETAR)\]|\{\{|lorem ipsum", flat, re.I):
                errors.append("unfinished text ([TO COMPLETE], {{placeholder}} or Lorem ipsum)")
            for t in a.missing:
                if present(t, flat):
                    errors.append(f"'{t}' is in the missing list but appears in the document")
            if profile is not None:
                for t in watch:
                    if present(t, flat) and not present(t, profile):
                        errors.append(f"'{t}' appears but is not in the profile")
            for b in banned:
                if b in flat.lower():
                    errors.append(f"banned phrase: «{b}»")
            if is_letter:
                n = letter_body_words(txt, html_src)
                if n is None:
                    notes.append("NOT CHECKED: letter length (salutation/closing not found)")
                elif not a.min_words <= n <= a.max_words:
                    errors.append(f"letter body has {n} words (expected {a.min_words}–{a.max_words})")
                if a.employer and a.employer.lower() not in flat.lower():
                    errors.append(f"the employer '{a.employer}' is not named in the letter")
            # a capital letter cut from its word ("T he"); real one-letter words (A, I, O, Y) are not counted
            if re.search(r"(?<![A-Za-zÀ-ÿ])[B-HJ-NP-XZ] [a-zé]{2,}", txt):
                warns.append("split words in the extracted text (e.g. 'T he'): screening tools may misread it")
        if html_src:
            if is_letter and re.search(r"<(b|strong)\b", html_src.split('<div class="body">')[-1] if '<div class="body">' in html_src else html_src):
                errors.append("bold text in the letter")
            if not is_letter and re.search(r"<li>[^<]*<(b|strong)\b", html_src):
                warns.append("bold keywords inside bullet points (looks machine-made)")
        n_pages = pages(f)
        if n_pages is not None:
            limit = 1 if is_letter else 2
            if n_pages > limit:
                errors.append(f"{n_pages} pages (max {limit})")
        if not re.match(r"^(CV|Resume|Letter|Lettre|LM|Carta|Anschreiben|Lebenslauf)_[A-Za-z]+_[A-Za-z-]+_[A-Za-z0-9-]+_[A-Za-z0-9-]+\.(pdf|docx|html)$", name):
            warns.append("file name differs from CV_FirstName_LastName_Company_Position.pdf")
        status = "❌" if errors else "✅"
        print(f"{status} {name}" + (f"  ({'letter' if is_letter else 'CV'}, {n_pages} page(s))" if n_pages else f"  ({'letter' if is_letter else 'CV'})"))
        for e in errors:
            print(f"   ERROR  {e}")
        for w in warns:
            print(f"   warning {w}")
        for n in notes:
            print(f"   {n}")
        blocking += bool(errors)
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
