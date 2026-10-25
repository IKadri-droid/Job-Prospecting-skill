# Job Prospecting skill

[![tests](https://github.com/IKadri-droid/Job-Prospecting-skill/actions/workflows/tests.yml/badge.svg)](https://github.com/IKadri-droid/Job-Prospecting-skill/actions/workflows/tests.yml)

**You answer, it prepares. You approve, you apply.**

A skill for Claude that helps **anyone** prepare real job applications — any trade, any country, any background.
A short interview (fast mode in 3 questions, or 7 simple steps, one question at a time), then a profile, a base CV,
a CV and a cover letter **tailored to each offer**, a job search, spontaneous applications, a tracking table,
reminders, and an optional **mailbox setup** (Gmail, Outlook, Yahoo, iCloud, Proton or any other) to follow replies
and job alerts — **read-only**.


## Simple for the person, solid behind the scenes
The person only sees short questions, clear summaries and finished documents. Behind the scenes, Claude works with:
- **templates** — a one-column CV readable by screening tools (ATS) and a classic cover letter, never an improvised layout;
- **guides** — writing (bullets that prove something, keywords, banned stock phrases), CV customs for 15+ countries,
  job search (official sources, scoring, report format), mailbox setup per provider, a quality checklist;
- **scripts** (dependency-free Python, Windows/macOS/Linux) — fill templates safely, render PDFs, **check every
  document before the person sees it** (unfinished text, skills they don't have, certifications absent from their
  profile, stock phrases, letter length, page count), keep the tracking table and list reminders due in working days;
- **tests** — unit tests for the scripts (run on every push) and 10 behaviour cases in `evals/evals.json`.

## What it never does
- **Makes nothing up**: no skill, diploma or experience the person did not give. Missing items are marked [TO COMPLETE].
- **Sends nothing without approval**: every application and reminder is shown first and sent by the person.
- **Never asks for a password**, app password, token or ID document in the chat.
- **No automatic collection** from social networks or sites that forbid it (job alerts by e-mail are used instead).
- **No guessed contacts**, and respect for each country's laws and CV customs.
- **No false promises**: it says what is possible with the person's equipment (phone only, Claude app, Claude Code).

## Contents
| Path | What |
|---|---|
| `skills/job-prospecting/SKILL.md` | the skill: pace (fast/full), interview, rules, documents, search, applications |
| `skills/job-prospecting/references/` | `writing-guide`, `cv-formats-by-country`, `search-guide`, `email-integration`, `quality-checklist` |
| `skills/job-prospecting/templates/` | CV (one column), cover letter, profile, search report, tracking table |
| `skills/job-prospecting/scripts/` | `fill_template.py`, `render_pdf.py`, `check_documents.py`, `tracker.py` |
| `skills/job/SKILL.md` | optional shortcut: typing `/job` launches the interview |
| `examples/` | a fictional CV and letter (JSON → HTML → PDF) |
| `tests/`, `evals/` | script tests, behaviour cases |
| `build.sh` | builds `dist/job-prospecting.skill` and `dist/job.skill` to upload |

## Install
**Claude (web, desktop, mobile)** — run `./build.sh`, then *Settings → Capabilities → Skills → Upload skill* and
choose `dist/job-prospecting.skill` (and `dist/job.skill` for the `/job` shortcut). Skills must be enabled for your account.

**Claude Code** — copy the folders into your personal skills directory:
```bash
mkdir -p ~/.claude/skills
cp -r skills/job-prospecting skills/job ~/.claude/skills/
```
Then say "I'm looking for a job" (or `/job`).

## Use
Say what you are looking for, in any language ("je cherche une alternance", "I need a summer job", "busco trabajo",
"ich suche eine Ausbildung"…). The skill starts in English, asks which language you want for the conversation and for
the documents, then whether you want to go fast or take 15 minutes. You can answer "skip" at any time and pick up
later where you left off.

## Develop
```bash
python3 tests/test_scripts.py                      # script tests (no PDF engine needed)
python3 skills/job-prospecting/scripts/render_pdf.py --which   # PDF engines found on this computer
```

## License
MIT — see `LICENSE`.
