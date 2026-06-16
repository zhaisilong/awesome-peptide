---
name: curate-peptide-papers
description: Curate the awesome-peptide paper list. Use when Codex needs to pull latest notes from the vendor/paper-read submodule, scan paper-read for peptide-related papers, enrich paper metadata through Crossref or arXiv, find, verify, add, classify, deduplicate, or update peptide deep-learning papers in data/paper.csv or data/paper-read.csv; manage DOI, code, dataset, blog, quality, pinned, abstract, or tag metadata; regenerate README.md from the CSV sources; or validate paper-list consistency for this repository.
---

# Curate Peptide Papers

Use this skill for content curation in `awesome-peptide`. The manually curated paper data lives in `data/paper.csv`; paper-read sourced entries live in minimal form in `data/paper-read.csv`; `README.md` is generated from both CSV sources plus `DATABASE.md` and the Liquid templates. `vendor/paper-read` is the local submodule source for discovering newly reviewed paper notes.

## Quick Start

1. Inspect the worktree before changing content:
```bash
git status --short
```

2. Read the relevant references:
- `references/repo-content-map.md` for source files and generation flow.
- `references/paper-curation.md` for CSV field rules and curation policy.
- `references/paper-read-source.md` when scanning the `paper-read` submodule.

3. Edit `data/paper.csv` or `data/paper-read.csv`, then validate and regenerate:
```bash
pip install -e .
awe-check
awe-pep
git diff -- data/paper.csv README.md
```

If the command names are unavailable, run the modules directly after installing dependencies:
```bash
python -m awepep.check
python -m awepep.main
```

## Paper-Read Workflow

Use this workflow when the user asks to pull latest papers from `paper-read` or scan for peptide papers:

```bash
git submodule update --init --recursive
git submodule update --remote vendor/paper-read
python .codex/skills/curate-peptide-papers/scripts/scan_paper_read_candidates.py --limit 200 --enrich-crossref
```

Then automatically curate high-confidence candidates into `data/paper-read.csv`:

1. Review the scanner Markdown and JSON reports.
2. Skip candidates already present by DOI.
3. Verify DOI, code/data links, and peptide/deep-learning relevance from the note plus primary sources.
4. Choose `sec` and `subsec` from the current README taxonomy; bibliographic metadata must not be used as a substitute for classification.
5. Add clear candidates to `data/paper-read.csv` with `doi,title,source,sec,subsec,code,dataset,quality,pined,tags`.
6. Let README generation fetch authors, venue, publish date, DOI link, and abstract from Crossref or the arXiv fallback.
7. Run `awe-check` and the no-write generation smoke test.
8. Summarize added and skipped candidates.

Do not edit files inside `vendor/paper-read`; it is an external source submodule.

## Curation Workflow

For adding or updating papers:

1. Verify bibliographic metadata from primary sources. Prefer DOI landing pages, arXiv/bioRxiv, journal pages, PubMed, Crossref, and official code or dataset repositories. Browse for recent papers or any metadata that could have changed.
2. Check for an existing entry by DOI and title before adding a row.
3. Classify with the exact current section/subsection values from `awepep/config.py`.
4. Keep `publications` in Markdown DOI-link form so `awepep.check` can extract the DOI.
5. Default optional fields to blank. Use `quality=high` only for clearly important work. Use `pined=true` only for selected important papers and keep the count below `max_pined = 30`.
6. Prefer short, slash-separated tags. Existing tags that match `awepep/config.py` authors or tools render as links automatically.
7. Regenerate `README.md` only after CSV edits, then inspect the diff.

For `data/paper-read.csv`, keep only the minimal source row. Required decision fields are DOI and the agent-selected `sec/subsec`; optional `title`, `source`, `code`, `dataset`, `quality`, `pined`, and `tags` help display or audit the row. Use conservative official source links only.

## CSV Row Drafts

Use the helper to produce a correctly ordered row without mutating `data/paper.csv`:

```bash
python .codex/skills/curate-peptide-papers/scripts/draft_paper_row.py \
  --title "Example peptide design paper" \
  --sec "Peptide Design & Generation" \
  --subsec "Structure-Based Design" \
  --authors "A. Author, B. Author" \
  --venue JCIM \
  --doi 10.1021/example \
  --publish-date 2026-6-16 \
  --code-label GitHub \
  --code-url https://github.com/example/project \
  --tags "Diffusion/Cyclic"
```

Review the printed row before appending it to `data/paper.csv`.

## Guardrails

- Do not hand-edit generated paper sections in `README.md`; edit `data/paper.csv` and regenerate.
- Do not add papers without a DOI unless the user explicitly accepts that `awepep.check` will need to change.
- Do not put generated authors, venue, date, publication link, or abstract into `data/paper-read.csv`; those are generated live.
- Do not invent new section or subsection labels during paper-add tasks.
- If dependencies are missing, install the package in editable mode before validating.
- If `README.md` generation fails for a paper-read DOI, verify the DOI with Crossref, arXiv, or the DOI landing page before changing classification or source rows.

## References

- Read `references/paper-curation.md` before editing `data/paper.csv`.
- Read `references/repo-content-map.md` when locating source files or explaining the generation flow.
- Read `references/paper-read-source.md` before using the paper-read scanner or submodule.
