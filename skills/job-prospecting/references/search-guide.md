# Job search guide — sources, scoring, report

Read before any search. The search is a service to the person: precise, honest, never padded.

## Sources (pick with the person in Step 7)
1. **The national public employment service** of the country (always first; free, official), e.g. France Travail
   and La bonne alternance (France), Bundesagentur für Arbeit (Germany), Find a job (UK), USAJOBS for federal jobs
   and state job banks (USA), Job Bank (Canada), SEPE/Empleate (Spain), ANAPEC (Morocco). Verify the current name
   and address online: they change.
2. **General job boards** active in that country (Indeed, local leaders such as HelloWork, StepStone, Seek,
   InfoJobs, Welcome to the Jungle…).
3. **Trade-specific sites** (healthcare, hospitality, construction, IT, public sector, agriculture, NGOs).
4. **Careers pages** of employers in the area, temp agencies, apprenticeship/work-study portals, schools' job boards.
5. **Job alerts received by e-mail** (`email-integration.md`): read them first, then verify each offer elsewhere.
Never open sites that forbid automatic access (LinkedIn and similar): use their e-mail alerts instead, and verify
the offer on the employer's site or another board.

Effort: at least 10–15 different searches covering every area and every target job title before concluding.
Open each offer to check it is still online; if it cannot be read, keep it marked "not verified" rather than
inventing details.

## What rules an offer out (and only this)
The person's own choices (contract type, area, trade, refusals, conditions), a legal impossibility (work
authorization, a licence required by law), school or training ads that recruit students (not employers), duplicates.
**Never** the person's level: a gap goes in "what you are missing", not in a refusal.
If the person chose "as many as possible", an offer with the wrong contract type (e.g. a permanent job for someone
looking for work-study) is not discarded: the organization goes to the spontaneous applications list.

## Score out of 100 (to rank, never to filter)
- 40 — requirements of the offer proven by the profile
- 20 — closeness to the person's priority targets
- 15 — place, hours and rhythm compatible
- 15 — achievements usable as proof
- 10 — nice-to-haves covered
Justify each score in one line.

## Spontaneous applications (if "as many as possible")
Organizations of every size and type that plausibly need the person's trade, with or without a posting: public
services (town halls, hospitals, fire services, schools), associations, small and new businesses (business
incubators, local chambers of commerce directories), large employers. For each: a **public proof** of the need
(a service, a past or current posting, a product, a team page) and a **published way to apply** (careers page,
recruitment e-mail, contact form). Never guess an address.

## Report format (`templates/search-report-template.md`)
For each offer, a section starting with `### <employer> — <job title>`, immediately followed by:
- `- [x] Prepare CV + letter` (or `- [ ]`), then one data line
  `<!-- offer: {"employer": "…", "title": "…", "place": "…", "url": "…", "source": "…", "contact": "…"} -->`
  (valid JSON on one line; `contact` = published e-mail or link, else "no published contact").
Then: place, dates (publication, start, length if published), the mission in 2–3 sentences in the posting's words,
what you have / what you are missing (with the profile's validated sentences), achievements and keywords to put
forward, how to apply, score and justification.

Spontaneous section: title `## Spontaneous applications`, each organization `### <organization>` followed by
`- [x] Prepare letter (spontaneous)` and
`<!-- organization: {"employer": "…", "sector": "…", "place": "…", "url": "…", "source": "…", "contact": "…"} -->`,
then the public reason they may need the person and how to apply.

End: ruled-out offers with the precise reason, number found, sources consulted, problems met. If the market is
small, say so plainly; do not widen the criteria without the person's agreement.
