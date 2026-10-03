# Generated README Rules

Use this reference before editing `README.md`, `awepep/template.py`, or `awepep/paper.py`.

## Source Of Truth

- Paper entries come from `data/paper.csv` and minimal `data/paper-read.csv` rows enriched by the tracked metadata snapshot.
- Chapter 0 content comes from `DATABASE.md`.
- Header, table of contents, paper formatting, cover image, contribution text, related links, and citations come from `awepep/template.py`.
- Generation orchestration comes from `awepep/paper.py`.

## Do Not Hand-Edit Generated Sections

Avoid direct edits to generated paper sections in `README.md`. Instead:

- Edit `data/paper.csv` for paper metadata.
- Edit `data/paper-read.csv` for note-sourced editorial fields and refresh its metadata snapshot explicitly.
- Edit `DATABASE.md` for Chapter 0 manually maintained content.
- Edit `awepep/template.py` for presentation changes.
- Edit `awepep/paper.py` for generation logic changes.

## Regeneration Risk

`README.md` starts with update-frequency, MolAstra, and Codex-agent automation notes. These notes live in `awepep/template.py`; before accepting a README regeneration diff, check that they remain present.

## Diff Review Checklist

After regenerating:

```bash
git diff -- README.md
```

Check for:

- Unintended deletion of the top note.
- Unexpected table of contents anchor changes.
- Large paper ordering changes not explained by date or taxonomy edits.
- Missing abstracts, code links, dataset links, blog links, tags, or pinned papers.
- Markdown escaping or CSV quoting mistakes rendered into the README.
- Section/subsection order that differs from config, including mixed publication dates.
- Future publications incorrectly appearing in the recent section.
- Partial dates converted into invented January 1 dates or actual false pinned flags treated as true.
- Chapter 0 papers duplicated outside the canonical CSV list.

Render `awe-pep --offline --as-of YYYY-MM-DD` for reproducible review. Missing snapshots must fail rather than silently discard papers; refresh fallback must warn. Escape abstracts in HTML details blocks. Compare TOC targets with the punctuation-stripped GitHub heading slugs.

## No-Write Smoke Test

Use this when validating generator imports or output shape without modifying `README.md`:

```bash
python - <<'PY'
from awepep.paper import PaperList
md = PaperList("data/paper.csv", offline=True).get_md(write=False)
print(len(md), md.splitlines()[0])
PY
```
