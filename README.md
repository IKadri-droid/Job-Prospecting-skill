# Job Prospecting skill

A skill for Claude that helps **anyone** prepare their job applications — any trade, any country, any background:
a short interview (7 steps, one simple question at a time), then a profile, a base CV, CVs and cover letters
tailored to each offer, a daily job search, a tracking table, reminders, and an optional **mailbox setup**
(Gmail, Outlook, Yahoo, iCloud, Proton or any other provider) to follow replies and job alerts — **read-only**.

> 🇫🇷 Un skill pour Claude qui aide n'importe qui à préparer ses candidatures, quel que soit le métier ou le pays :
> un entretien en 7 étapes (une question simple à la fois), puis profil, CV de base, CV et lettres adaptés à chaque
> offre, recherche d'offres, suivi, relances, et en option l'accompagnement de la boîte mail (Gmail, Outlook, Yahoo,
> iCloud, Proton ou autre) pour suivre les réponses et les alertes emploi, **en lecture seule**.

## What it never does
- **Makes nothing up**: no skill, diploma or experience the person did not give. Missing items are marked [TO COMPLETE].
- **Sends nothing without approval**: every application and reminder is shown first and sent by the person.
- **Never asks for a password**, app password, token or ID document in the chat.
- **No automatic collection** from social networks or sites that forbid it (job alerts by e-mail are used instead).
- **No guessed contacts**, and respect for each country's laws and CV customs.

## Contents
| Path | What |
|---|---|
| `skills/job-prospecting/SKILL.md` | the skill: interview, rules, documents, search, applications |
| `skills/job-prospecting/references/email-integration.md` | mailbox setup per provider (folders and rules, read-only automatic reading, job alerts, matching replies, revoking access) |
| `skills/job/SKILL.md` | optional shortcut: typing `/job` launches the interview |
| `build.sh` | builds `dist/job-prospecting.skill` and `dist/job.skill` to upload |

## Install
**Claude (web, desktop, mobile)** — run `./build.sh`, then *Settings → Capabilities → Skills → Upload skill* and
choose `dist/job-prospecting.skill` (and `dist/job.skill` for the `/job` shortcut). Skills must be enabled for your account.

**Claude Code** — copy the folders into your personal skills directory:
```bash
mkdir -p ~/.claude/skills
cp -r skills/job-prospecting skills/job ~/.claude/skills/
```
Then start a conversation with "I'm looking for a job" (or `/job`).

## Use
Just say what you are looking for, in any language ("je cherche une alternance", "I need a summer job",
"busco trabajo"…). The skill starts in English, then asks which language you want for the conversation and for the
documents. You can answer "skip" at any time, and pick up later where you left off.

## License
MIT — see `LICENSE`.
