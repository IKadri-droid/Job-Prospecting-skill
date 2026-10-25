#!/usr/bin/env python3
"""Tests of the skill scripts (standard library only): python3 tests/test_scripts.py"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "job-prospecting"
EX = ROOT / "examples"


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=cwd)


class FillTemplate(unittest.TestCase):
    def fill(self, data, template="cv-one-column.html"):
        with tempfile.TemporaryDirectory() as d:
            j, out = Path(d, "d.json"), Path(d, "out.html")
            j.write_text(json.dumps(data), encoding="utf-8")
            r = run(SKILL / "scripts/fill_template.py", SKILL / "templates" / template, j, "-o", out)
            return r, (out.read_text(encoding="utf-8") if out.exists() else "")

    def sample(self):
        return json.loads((EX / "sample-cv.json").read_text(encoding="utf-8"))

    def test_sample_ok_and_empty_section_removed(self):
        r, html = self.fill(self.sample())
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("{{", html)
        self.assertNotIn("<h2>Projects", html)

    def test_text_is_escaped(self):
        d = self.sample(); d["headline"] = "<script>x</script>"
        r, html = self.fill(d)
        self.assertIn("&lt;script&gt;", html)

    def test_refuses_dangerous_tag(self):
        d = self.sample(); d["summary"] = "<p>Hi<img src=x></p>"
        self.assertNotEqual(self.fill(d)[0].returncode, 0)

    def test_refuses_unfinished(self):
        d = self.sample(); d["summary"] = "<p>[TO COMPLETE]</p>"
        self.assertNotEqual(self.fill(d)[0].returncode, 0)

    def test_refuses_missing_value(self):
        d = self.sample(); del d["headline"]
        self.assertNotEqual(self.fill(d)[0].returncode, 0)


class CheckDocuments(unittest.TestCase):
    def letter(self, body_extra=""):
        data = json.loads((EX / "sample-letter.json").read_text(encoding="utf-8"))
        data["body"] = data["body"].replace("<p>Your offer", f"<p>{body_extra}Your offer", 1)
        d = tempfile.mkdtemp()
        j, out = Path(d, "d.json"), Path(d, "Letter_Sam_Example_ExampleBakery_ApprenticeBaker.html")
        j.write_text(json.dumps(data), encoding="utf-8")
        r = run(SKILL / "scripts/fill_template.py", SKILL / "templates/cover-letter.html", j, "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        return out

    def check(self, f, *extra):
        return run(SKILL / "scripts/check_documents.py", f, "--profile", EX / "sample-profile.md", *extra)

    def test_good_letter_passes(self):
        r = self.check(self.letter(), "--employer", "Example Bakery", "--lang", "en")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_missing_requirement_blocked(self):
        r = self.check(self.letter("I hold a food hygiene certificate. "), "--missing", "food hygiene certificate")
        self.assertEqual(r.returncode, 1); self.assertIn("missing list", r.stdout)

    def test_unknown_certification_blocked(self):
        r = self.check(self.letter("My TOEIC score is high. "))
        self.assertEqual(r.returncode, 1); self.assertIn("TOEIC", r.stdout)

    def test_banned_phrase_blocked(self):
        r = self.check(self.letter("I am passionate about bread. "), "--lang", "en")
        self.assertEqual(r.returncode, 1); self.assertIn("banned", r.stdout)

    def test_wrong_employer_blocked(self):
        r = self.check(self.letter(), "--employer", "Another Company")
        self.assertEqual(r.returncode, 1)


class AdaptCv(unittest.TestCase):
    def adapt(self, changes):
        with tempfile.TemporaryDirectory() as d:
            j, out = Path(d, "a.json"), Path(d, "out.html")
            j.write_text(json.dumps(changes), encoding="utf-8")
            r = run(SKILL / "scripts/adapt_cv.py", EX / "own-cv-base.html", j, "-o", out)
            return r, (out.read_text(encoding="utf-8") if out.exists() else "")

    def test_only_zones_change_and_design_kept(self):
        r, html = self.adapt({"headline": "<p>Apprentice baker — work-study from September</p>",
                              "interests": "<li>Cooking for friends</li><li>Cycling</li>"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Apprentice baker", html)
        self.assertIn("grid-template-columns:60mm", html)      # the person's own design is untouched

    def test_refuses_unknown_zone(self):
        self.assertNotEqual(self.adapt({"photo": "<p>x</p>"})[0].returncode, 0)

    def test_refuses_bold_and_links(self):
        self.assertNotEqual(self.adapt({"skills": "<ul><li><strong>SAP</strong></li></ul>"})[0].returncode, 0)
        self.assertNotEqual(self.adapt({"skills": "<ul><li><a href='x'>x</a></li></ul>"})[0].returncode, 0)


class Tracker(unittest.TestCase):
    def test_flow(self):
        with tempfile.TemporaryDirectory() as d:
            t = SKILL / "scripts/tracker.py"
            self.assertEqual(run(t, "add", "--employer", "Example Bakery", "--title", "Apprentice", cwd=d).returncode, 0)
            self.assertNotEqual(run(t, "add", "--employer", "Example Bakery", "--title", "Apprentice", cwd=d).returncode, 0)
            ident = Path(d, "tracking.csv").read_text(encoding="utf-8").splitlines()[1].split(",")[0]
            run(t, "set", ident, "status=sent", "sent_on=2026-11-02", cwd=d)          # a Monday
            self.assertNotIn(ident, run(t, "due", "--today", "2026-11-10", cwd=d).stdout)
            self.assertIn("2026-11-11", run(t, "due", "--today", "2026-11-11", cwd=d).stdout)
            Path(d, "h.txt").write_text("2026-11-11\n", encoding="utf-8")
            self.assertIn("2026-11-12", run(t, "due", "--today", "2026-11-12", "--holidays", "h.txt", cwd=d).stdout)
            run(t, "set", ident, "reminder_on=2026-11-12", cwd=d)
            self.assertNotEqual(run(t, "set", ident, "reminder_on=2026-11-13", cwd=d).returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
