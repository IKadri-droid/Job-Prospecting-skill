# Quality checklist — before the person sees a document

Go through it for every CV and every letter. With a computer, run the script first; then check the rest yourself.

```bash
python3 scripts/check_documents.py CV_….pdf Letter_….pdf --profile profile.md \
    --missing "Forklift licence" "SAP" --letter-file Letter_….pdf --employer "Company" --lang en
```

## Truth (rule 1)
- [ ] Every skill, diploma, licence, tool, language level and number comes from `profile.md` or the offer.
- [ ] No item of the offer's "missing" list appears as acquired (script: `--missing`).
- [ ] Skill levels use the person's validated sentences, unchanged.
- [ ] School and personal projects are presented as such, never as paid work.
- [ ] No [TO COMPLETE], no `{{placeholder}}`, no "Lorem", no other company's name left from a previous application.

## Fit with the offer
- [ ] The CV title and summary use the offer's job title and 2–3 mission phrases.
- [ ] The most relevant skills and achievements come first.
- [ ] Letter paragraph 1 cites something real from the posting (or, spontaneous, from the organization's public info).

## Form
- [ ] CV: one column, real selectable text, standard section titles, consistent dates, 1–2 pages per country custom.
- [ ] Letter: 250–300 words in three paragraphs (or the country's custom), one page, subject line, no bold.
- [ ] No banned phrase (`writing-guide.md` §3); no keyword in bold.
- [ ] Contact details correct and identical on CV and letter; the person's chosen e-mail address.
- [ ] File names: `CV_FirstName_LastName_Company_Position.pdf`, `Letter_FirstName_LastName_Company_Position.pdf`.
- [ ] Country customs applied (photo, personal details, length) and the choice explained to the person once.

## Honesty
- [ ] If a check could not be run (no PDF tool, no script), say so to the person instead of claiming it passed.
