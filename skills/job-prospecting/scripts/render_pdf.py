#!/usr/bin/env python3
"""Render HTML documents to PDF with the best engine available on this computer (no install required by the skill).

Usage: python3 render_pdf.py CV_….html Letter_….html          (writes CV_….pdf, Letter_….pdf next to them)
       python3 render_pdf.py --which                           (lists the engines found)

Engines tried in order: Chrome / Chromium / Edge / Brave (headless), WeasyPrint (Python module or command),
wkhtmltopdf. Set the CHROME environment variable to a browser path to force one. If none is found, the script
explains how to save the HTML as PDF from any browser (File → Print → Save as PDF) and exits with code 2.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge",
                "microsoft-edge-stable", "brave-browser", "chrome", "msedge"]
CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for n in CHROME_NAMES:
        if shutil.which(n):
            return shutil.which(n)
    return next((p for p in CHROME_PATHS if Path(p).exists()), None)


def engines():
    found = []
    if find_chrome():
        found.append("chrome")
    try:
        import weasyprint  # noqa: F401
        found.append("weasyprint-module")
    except Exception:
        if shutil.which("weasyprint"):
            found.append("weasyprint")
    if shutil.which("wkhtmltopdf"):
        found.append("wkhtmltopdf")
    return found


def render(html_file, pdf_file, engine):
    src = Path(html_file).resolve()
    if engine == "chrome":
        with tempfile.TemporaryDirectory() as profile:
            subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
                            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
                            f"--user-data-dir={profile}", f"--print-to-pdf={Path(pdf_file).resolve()}", src.as_uri()],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    elif engine == "weasyprint-module":
        import weasyprint
        weasyprint.HTML(filename=str(src)).write_pdf(str(pdf_file))
    elif engine == "weasyprint":
        subprocess.run(["weasyprint", str(src), str(pdf_file)], check=True, timeout=120)
    elif engine == "wkhtmltopdf":
        subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "-s", "A4", str(src), str(pdf_file)],
                       check=True, timeout=120)
    if not Path(pdf_file).exists() or Path(pdf_file).stat().st_size == 0:
        raise RuntimeError("no PDF produced")


def utf8_output():
    """Windows consoles may not be UTF-8: never crash on ✅ or accented text."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    utf8_output()
    if "--which" in sys.argv:
        print("engines found:", ", ".join(engines()) or "none")
        return
    files = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not files:
        sys.exit(__doc__)
    found = engines()
    if not found:
        print("No PDF engine found on this computer. Open each HTML file in a browser, then File → Print →"
              " 'Save as PDF' (A4, no headers and footers, margins: default).")
        sys.exit(2)
    for f in files:
        out = str(Path(f).with_suffix(".pdf"))
        for e in found:
            try:
                render(f, out, e)
                print(f"written: {out} (via {e})")
                break
            except Exception as exc:
                print(f"  {e} failed on {f}: {exc}")
        else:
            sys.exit(f"could not render {f}")


if __name__ == "__main__":
    main()
