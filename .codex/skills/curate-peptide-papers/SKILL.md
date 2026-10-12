---
name: curate-peptide-papers
description: Curate peptide papers primarily from the paper-read submodule, verify formal publication, classify and tag CSV entries, archive preprints and regenerate README offline. Use for paper-read updates and small AIDD-focused discovery supplements.
---

# Curate Peptide Papers

Use paper-read as the primary, owner-curated source. Include substantive peptide research across computational and experimental domains. README is generated, and the vendor submodule is read-only.

## Choose The Workflow

- For discovery and classification, read [paper-curation.md](references/paper-curation.md).
- For note scans and source rows, read [paper-read-source.md](references/paper-read-source.md).
- For file ownership and generation, read [repo-content-map.md](references/repo-content-map.md).

Inspect `git status --short` and the current `awepep.config.sections`/`tag_groups` before editing. Do not infer permission to commit, push, merge or schedule from a paper-discovery request.

## Update Paper-Read First

```bash
git submodule update --init --recursive
git -C vendor/paper-read rev-parse HEAD
git submodule update --remote vendor/paper-read
git -C vendor/paper-read rev-parse HEAD
awe-discover --limit 200
```

Compare the old/new submodule commits and review changed notes first, including changes to accepted or archived papers. Then scan for historical omissions. Paper-read has no publication-window cutoff: insert older work by its actual publication date. Note month is only a triage hint. Read the source reference for duplicate-inclusive rescans and metadata refresh.

## Small Discovery Supplement

After paper-read review, independently discover at most **3 accepted papers per run**, targeting 2-3 only when worthwhile work exists. Prefer AIDD; an exceptional purely experimental paper needs an explicit significance rationale. Paper-read additions, historical migrations and verification requests do not consume this quota. Count supplements across all providers together; do not fill a quota with weak work.

Default discovery scans paper-read only. Crossref/PubMed discovery requires explicit `--sources` and a publication window; use targeted searches rather than a broad survey. `--limit` caps retrieved candidates, not accepted papers. Inspect errors/truncation and keep retries bounded. Do not create scheduled paper-adding Actions.

## Curate

1. Review candidate title, abstract and primary source for substantive peptide relevance. AI is not required.
2. Accept only verified formal journal/conference publications or credible institutional technical reports. No ordinary arXiv/bioRxiv preprints; a preprint is not a technical report merely because it is named one.
3. Verify DOI or official stable HTTPS URL and publication date. Deduplicate DOI/URL/title and preprint/formal relationships across active tables and the archive. Never substitute note, acceptance or API registration dates.
4. Choose one primary contribution-based section/subsection from config. Use canonical tags for secondary topics.
5. Keep DOI-backed paper-read rows minimal. Put DOI-less formal papers in `data/paper.csv`, preserving the paper-read link in `blogs`. Archive unverified preprints in `data/paper-archive.csv`; upgrade archived work when a formal version is verified. Do not blindly append scanner output or assign flags without evidence.
6. Refresh metadata snapshots for paper-read changes, then validate and regenerate offline with a fixed reference date.
7. Report paper-read additions, independent supplements (0-3), formal-version upgrades, archived records, unresolved evidence and coverage limits separately, with source links.

## Validate And Render

```bash
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py --strict
python -m unittest discover -s tests -v
awe-pep --refresh-metadata --as-of YYYY-MM-DD
awe-pep --offline --as-of YYYY-MM-DD
git diff -- data README.md
```

Replace `YYYY-MM-DD` with the review date. Use `PaperList("data/paper.csv", offline=True).get_md(write=False)` for read-only verification. Never hand-edit generated paper sections or files inside `vendor/paper-read`.
