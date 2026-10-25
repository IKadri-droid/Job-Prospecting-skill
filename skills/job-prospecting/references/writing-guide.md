# Writing guide — CVs and cover letters that get read

Read before writing any CV or letter. Everything here applies in any language; translate the examples.
Rule 1 of the skill always wins: only facts from `profile.md` or from the offer.

## 1. Read the offer like a recruiter (do this first, every time)

From the posting, extract into a short working note (not shown to the person unless asked):
- **Must-haves**: diplomas, licenses, years, tools, languages the offer clearly requires.
- **Nice-to-haves**: "a plus", "appreciated", "ideally".
- **The mission in their words**: 3–5 key phrases describing the daily work (they feed the CV title, the summary
  and the first paragraph of the letter).
- **Keywords**: the exact terms a screening tool or a hurried recruiter will look for (job title, tools, methods).
- **Missing**: every must-have or nice-to-have that `profile.md` does not prove. This list is passed to
  `scripts/check_documents.py --missing` so none of it can appear as acquired.

## 2. Tailor the CV (only the adaptable zones)

| Zone | How |
|---|---|
| Title | the offer's job title (or the closest honest one) + contract + availability, e.g. "Apprentice electrician — 2-year work-study from September" |
| Summary (2–3 lines) | who they are + what they want, reusing 2–3 key phrases of the mission; no adjectives they did not give |
| Skills | reorder so the offer's keywords come first; use the person's validated sentence ("I do it regularly"…) as the level; never a percentage, star or bar |
| Achievements / experience | keep the 2–4 most relevant first; each entry starts with the **job title** (see below); rewrite bullets with the offer's vocabulary when it describes what they really did |
| Interests (optional) | only the ones the person accepted to show; put first the one closest to the job or the employer |

Everything else stays identical to the base CV.

### Title first: recruiters read the role before the numbers
Recruiters scan the **job title and level of responsibility** first ("Head chef", "Sous-chef", "Team leader",
"Nurse's aide", "Site foreman"): it tells them in one second what the person can take on. Figures come after, to
support the title, never to replace it.
- Each experience starts with the title **as the employer would name it**, then the organization and dates:
  "**Head chef** — Example Bistro, Lyon — 2022–2025".
- The title must be the real one. If the person did the job without the title (e.g. ran the kitchen alone on
  weekends), never upgrade the title: describe the responsibility instead ("Cook — in charge of the kitchen on
  weekends, team of 3"). An honest acting role can be written only if the person confirms it ("Acting head chef").
- In the summary and the CV headline, lead with the role too: "Head chef with 8 years in bistro cooking", not
  "Cook who prepared 200 meals a day".
- Then the bullets give the scope and results that make the title credible.

### Bullets that prove something
Formula: **action verb + what + for whom/with what + result or scale** (only if the person gave it). Responsibility
first (who they managed, what they were in charge of), volume second.
- Weak: "Responsible for the kitchen." → Strong: "Led a kitchen team of 4 and designed the weekly menu; about 120 covers a day."
- Weak: "Customer service." → Strong: "Welcomed and advised about 60 customers a day; handled returns and payments."
- Weak: "School project in web development." → Strong: "School project: built a booking website with a teammate (HTML, CSS, a database), presented to 30 people."
Never invent a number. If the person has no figure, describe the scope ("every morning", "alone on weekends").

### Keywords and screening tools (ATS)
- Use the offer's exact terms when they are true ("forklift licence" if the offer says so, not only "forklift").
- One column, real text, standard section titles (Experience, Education, Skills, Languages — in the document
  language), dates in one consistent format, no table, no text in images, no icons replacing words
  ("Phone:", "E-mail:"), no header/footer holding key information.
- No keyword stuffing, no hidden white text: it is dishonest and many tools penalize it.
- Bold is for structure only (job titles, company names, section titles), never for sprinkled keywords: bold
  keywords look machine-made and put recruiters off.

## 3. The cover letter

**Length**: 250–300 words for the three body paragraphs (adapt to the country: shorter in the US/UK, a formal
structure in France/Germany — see `cv-formats-by-country.md`). **One page.** Plain text, no bold.

**Layout (classic)**: sender block top left (name, town, phone, e-mail), employer block on the right
(organization, department or person if published, town), place and date, subject line, salutation, three
paragraphs, closing formula, signature at the bottom.

**Subject line**: "Application — <job title> — <contract/start>"; for a spontaneous application:
"Spontaneous application — <field/trade> — <contract/start>".

**Paragraph 1 — why them**: one precise element **from the posting** (or, for a spontaneous application, from
the organization's public information): a mission, a product, a service, a value they state. Say why it matters
to the person. Never a fact you cannot point to.

**Paragraph 2 — proof**: the two achievements of the profile closest to the offer, each linked to one requirement,
told as what the person learned or did (a short story), not a list of tools copied from the CV.

**Paragraph 3 — practical + next step**: availability, contract, rhythm (for work-study), mobility (licence,
transport) when relevant, one real quality shown by an experience, and a proposal to meet. The quality comes only
from what the person validated (their own soft skills, or facts of their experience such as "trained new staff");
never an invented trait like "calm under pressure".

**Spontaneous application**: never pretend to answer an offer; say what you noticed about the organization and
what you can bring; ask whether an opening could exist now or later.

### Banned phrases (and their cousins in other languages)
"I am passionate about…", "dynamic and motivated", "I am the ideal candidate", "since I was a child",
"I would be a great asset", "please do not hesitate to contact me", "think outside the box", "team player"
without a fact, "hard-working" without a fact.
French: « passionné depuis toujours », « dynamique et motivé », « je suis le candidat idéal », « n'hésitez pas à me
contacter », « véritable atout », « force de travail ».
Replace every adjective by a fact from the profile.

## 4. Tone
Follow the tone chosen in Step 7 (very formal / direct / warm) and the phrases the person hates. Vouvoiement /
formal "you" wherever the language has it, unless the person asks otherwise. Short sentences beat long ones.

## 6. Interests and the recruiter (only with the person's copy of a public profile)
Goal: a natural common point with the person who recruits, never flattery.
1. List the recruiter's interests from the public professional information the person copied (rule 6).
2. Compare them with the interests the person accepted to show (`profile.md`) — the only allowed source.
3. Few interests (1–3): put first the person's closest real interest, even if approximate (running ↔ trail).
   Many interests (4+): keep the simplest, most direct match, 2 at most. No match: keep the person's interests,
   ordered by relevance to the job.
4. Use the person's own wording, closest to the recruiter's vocabulary.
Never: add an interest the person does not have, mention the recruiter or their tastes in the CV or the letter
("like you, I love…"), or store the recruiter's name anywhere shared. Possible conversation topics for an interview
can be noted for the person only.

## 7. Before showing anything
Run `quality-checklist.md`. The person reads the final version, not a draft with mistakes.
